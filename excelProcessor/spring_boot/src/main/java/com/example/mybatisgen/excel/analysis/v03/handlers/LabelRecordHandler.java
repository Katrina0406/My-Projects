package com.example.mybatisgen.excel.analysis.v03.handlers;

import org.apache.poi.hssf.record.LabelRecord;
import org.apache.poi.hssf.record.Record;

import com.example.mybatisgen.excel.analysis.v03.IgnorableXlsRecordHandler;
import com.example.mybatisgen.excel.context.xls.XlsReadContext;
import com.example.mybatisgen.excel.enums.RowTypeEnum;
import com.example.mybatisgen.excel.metadata.CellData;

/**
 * Record handler
 *
 * @author Dan Zheng
 */
public class LabelRecordHandler extends AbstractXlsRecordHandler implements IgnorableXlsRecordHandler {
    @Override
    public void processRecord(XlsReadContext xlsReadContext, Record record) {
        LabelRecord lrec = (LabelRecord)record;
        String data = lrec.getValue();
        if (data != null && xlsReadContext.currentReadHolder().globalConfiguration().getAutoTrim()) {
            data = data.trim();
        }
        xlsReadContext.xlsReadSheetHolder().getCellMap().put((int)lrec.getColumn(),
                CellData.newInstance(data, lrec.getRow(), (int)lrec.getColumn()));
        xlsReadContext.xlsReadSheetHolder().setTempRowType(RowTypeEnum.DATA);
    }
}
