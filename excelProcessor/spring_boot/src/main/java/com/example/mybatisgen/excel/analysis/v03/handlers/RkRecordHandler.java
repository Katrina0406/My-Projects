package com.example.mybatisgen.excel.analysis.v03.handlers;

import org.apache.poi.hssf.record.RKRecord;
import org.apache.poi.hssf.record.Record;

import com.example.mybatisgen.excel.analysis.v03.IgnorableXlsRecordHandler;
import com.example.mybatisgen.excel.context.xls.XlsReadContext;
import com.example.mybatisgen.excel.metadata.CellData;

/**
 * Record handler
 *
 * @author Dan Zheng
 */
public class RkRecordHandler extends AbstractXlsRecordHandler implements IgnorableXlsRecordHandler {

    @Override
    public void processRecord(XlsReadContext xlsReadContext, Record record) {
        RKRecord re = (RKRecord)record;
        xlsReadContext.xlsReadSheetHolder().getCellMap().put((int)re.getColumn(),
                CellData.newEmptyInstance(re.getRow(), (int)re.getColumn()));
    }
}
