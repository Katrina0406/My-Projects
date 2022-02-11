package com.example.mybatisgen.excel.analysis.v03.handlers;

import com.example.mybatisgen.excel.analysis.v03.IgnorableXlsRecordHandler;
import com.example.mybatisgen.excel.cache.ReadCache;
import com.example.mybatisgen.excel.context.xls.XlsReadContext;
import com.example.mybatisgen.excel.enums.RowTypeEnum;
import com.example.mybatisgen.excel.metadata.Cell;
import com.example.mybatisgen.excel.metadata.CellData;
import org.apache.poi.hssf.record.LabelSSTRecord;
import org.apache.poi.hssf.record.Record;

import java.util.Map;

/**
 * Record handler
 *
 * @author Dan Zheng
 */
public class LabelSstRecordHandler extends AbstractXlsRecordHandler implements IgnorableXlsRecordHandler {

    @Override
    public void processRecord(XlsReadContext xlsReadContext, Record record) {
        LabelSSTRecord lsrec = (LabelSSTRecord)record;
        ReadCache readCache = xlsReadContext.readWorkbookHolder().getReadCache();
        Map<Integer, Cell> cellMap = xlsReadContext.xlsReadSheetHolder().getCellMap();
        if (readCache == null) {
            cellMap.put((int)lsrec.getColumn(), CellData.newEmptyInstance(lsrec.getRow(), (int)lsrec.getColumn()));
            return;
        }
        String data = readCache.get(lsrec.getSSTIndex());
        if (data == null) {
            cellMap.put((int)lsrec.getColumn(), CellData.newEmptyInstance(lsrec.getRow(), (int)lsrec.getColumn()));
            return;
        }
        if (xlsReadContext.currentReadHolder().globalConfiguration().getAutoTrim()) {
            data = data.trim();
        }
        cellMap.put((int)lsrec.getColumn(), CellData.newInstance(data, lsrec.getRow(), (int)lsrec.getColumn()));
        xlsReadContext.xlsReadSheetHolder().setTempRowType(RowTypeEnum.DATA);
    }
}
