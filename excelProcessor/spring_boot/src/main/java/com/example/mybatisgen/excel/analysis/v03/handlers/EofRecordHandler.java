package com.example.mybatisgen.excel.analysis.v03.handlers;

import com.example.mybatisgen.excel.analysis.v03.IgnorableXlsRecordHandler;
import com.example.mybatisgen.excel.context.xls.XlsReadContext;
import com.example.mybatisgen.excel.enums.RowTypeEnum;
import com.example.mybatisgen.excel.metadata.Cell;
import com.example.mybatisgen.excel.read.metadata.holder.ReadRowHolder;
import com.example.mybatisgen.excel.read.metadata.holder.xls.XlsReadSheetHolder;
import org.apache.poi.hssf.record.Record;

import java.util.LinkedHashMap;

/**
 * Record handler
 *
 * @author Dan Zheng
 */
public class EofRecordHandler extends AbstractXlsRecordHandler implements IgnorableXlsRecordHandler {

    @Override
    public void processRecord(XlsReadContext xlsReadContext, Record record) {
        if (xlsReadContext.readSheetHolder() == null) {
            return;
        }
        // Sometimes tables lack the end record of the last column
        if (!xlsReadContext.xlsReadSheetHolder().getCellMap().isEmpty()) {
            XlsReadSheetHolder xlsReadSheetHolder = xlsReadContext.xlsReadSheetHolder();
            // Forge a termination data
            xlsReadContext.readRowHolder(new ReadRowHolder(xlsReadContext.xlsReadSheetHolder().getRowIndex() + 1,
                    xlsReadSheetHolder.getTempRowType(),
                    xlsReadContext.readSheetHolder().getGlobalConfiguration(), xlsReadSheetHolder.getCellMap()));
            xlsReadContext.analysisEventProcessor().endRow(xlsReadContext);
            xlsReadSheetHolder.setCellMap(new LinkedHashMap<Integer, Cell>());
            xlsReadSheetHolder.setTempRowType(RowTypeEnum.EMPTY);
        }

        xlsReadContext.analysisEventProcessor().endSheet(xlsReadContext);
    }
}
