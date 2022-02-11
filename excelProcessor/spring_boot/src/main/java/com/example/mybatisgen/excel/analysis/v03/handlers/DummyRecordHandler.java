package com.example.mybatisgen.excel.analysis.v03.handlers;

import com.example.mybatisgen.excel.analysis.v03.IgnorableXlsRecordHandler;
import com.example.mybatisgen.excel.context.xls.XlsReadContext;
import com.example.mybatisgen.excel.enums.RowTypeEnum;
import com.example.mybatisgen.excel.metadata.Cell;
import com.example.mybatisgen.excel.metadata.CellData;
import com.example.mybatisgen.excel.read.metadata.holder.ReadRowHolder;
import com.example.mybatisgen.excel.read.metadata.holder.xls.XlsReadSheetHolder;
import org.apache.poi.hssf.eventusermodel.dummyrecord.LastCellOfRowDummyRecord;
import org.apache.poi.hssf.eventusermodel.dummyrecord.MissingCellDummyRecord;
import org.apache.poi.hssf.record.Record;

import java.util.LinkedHashMap;

/**
 * Record handler
 *
 * @author Dan Zheng
 */
public class DummyRecordHandler extends AbstractXlsRecordHandler implements IgnorableXlsRecordHandler {
    @Override
    public void processRecord(XlsReadContext xlsReadContext, Record record) {
        XlsReadSheetHolder xlsReadSheetHolder = xlsReadContext.xlsReadSheetHolder();
        if (record instanceof LastCellOfRowDummyRecord) {
            // End of this row
            LastCellOfRowDummyRecord lcrdr = (LastCellOfRowDummyRecord)record;
            xlsReadSheetHolder.setRowIndex(lcrdr.getRow());
            xlsReadContext.readRowHolder(new ReadRowHolder(lcrdr.getRow(), xlsReadSheetHolder.getTempRowType(),
                    xlsReadContext.readSheetHolder().getGlobalConfiguration(), xlsReadSheetHolder.getCellMap()));
            xlsReadContext.analysisEventProcessor().endRow(xlsReadContext);
            xlsReadSheetHolder.setCellMap(new LinkedHashMap<Integer, Cell>());
            xlsReadSheetHolder.setTempRowType(RowTypeEnum.EMPTY);
        } else if (record instanceof MissingCellDummyRecord) {
            MissingCellDummyRecord mcdr = (MissingCellDummyRecord)record;
            xlsReadSheetHolder.getCellMap().put(mcdr.getColumn(),
                    CellData.newEmptyInstance(mcdr.getRow(), mcdr.getColumn()));
        }
    }
}
