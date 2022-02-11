package com.example.mybatisgen.excel.analysis.v03.handlers;

import org.apache.poi.hssf.record.BoundSheetRecord;
import org.apache.poi.hssf.record.Record;

import com.example.mybatisgen.excel.analysis.v03.IgnorableXlsRecordHandler;
import com.example.mybatisgen.excel.context.xls.XlsReadContext;

/**
 * Record handler
 *
 * @author Dan Zheng
 */
public class BoundSheetRecordHandler extends AbstractXlsRecordHandler implements IgnorableXlsRecordHandler {

    @Override
    public void processRecord(XlsReadContext xlsReadContext, Record record) {
        BoundSheetRecord bsr = (BoundSheetRecord)record;
        xlsReadContext.xlsReadWorkbookHolder().getBoundSheetRecordList().add((BoundSheetRecord)record);
    }
}
