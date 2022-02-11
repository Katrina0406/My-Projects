package com.example.mybatisgen.excel.analysis.v03.handlers;

import com.example.mybatisgen.excel.analysis.v03.IgnorableXlsRecordHandler;
import com.example.mybatisgen.excel.constant.BuiltinFormats;
import com.example.mybatisgen.excel.context.xls.XlsReadContext;
import com.example.mybatisgen.excel.enums.RowTypeEnum;
import com.example.mybatisgen.excel.metadata.CellData;
import org.apache.poi.hssf.record.NumberRecord;
import org.apache.poi.hssf.record.Record;

import java.math.BigDecimal;

/**
 * Record handler
 *
 * @author Dan Zheng
 */
public class NumberRecordHandler extends AbstractXlsRecordHandler implements IgnorableXlsRecordHandler {

    @Override
    public void processRecord(XlsReadContext xlsReadContext, Record record) {
        NumberRecord nr = (NumberRecord)record;
        CellData cellData = CellData.newInstance(BigDecimal.valueOf(nr.getValue()), nr.getRow(), (int)nr.getColumn());
        Integer dataFormat = xlsReadContext.xlsReadWorkbookHolder().getFormatTrackingHSSFListener().getFormatIndex(nr);
        cellData.setDataFormat(dataFormat);
        cellData.setDataFormatString(BuiltinFormats.getBuiltinFormat(dataFormat,
                xlsReadContext.xlsReadWorkbookHolder().getFormatTrackingHSSFListener().getFormatString(nr),
                xlsReadContext.readSheetHolder().getGlobalConfiguration().getLocale()));
        xlsReadContext.xlsReadSheetHolder().getCellMap().put((int)nr.getColumn(), cellData);
        xlsReadContext.xlsReadSheetHolder().setTempRowType(RowTypeEnum.DATA);
    }
}
