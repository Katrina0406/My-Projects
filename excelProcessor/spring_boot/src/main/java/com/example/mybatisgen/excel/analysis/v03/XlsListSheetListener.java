package com.example.mybatisgen.excel.analysis.v03;

import com.example.mybatisgen.excel.analysis.v03.handlers.BofRecordHandler;
import com.example.mybatisgen.excel.analysis.v03.handlers.BoundSheetRecordHandler;
import com.example.mybatisgen.excel.context.xls.XlsReadContext;
import com.example.mybatisgen.excel.exception.ExcelAnalysisException;
import org.apache.poi.hssf.eventusermodel.*;
import org.apache.poi.hssf.record.BOFRecord;
import org.apache.poi.hssf.record.BoundSheetRecord;
import org.apache.poi.hssf.record.Record;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

/**
 * In some cases, you need to know the number of sheets in advance and only read the file once in advance.
 *
 * @author Jiaju Zhuang
 */
public class XlsListSheetListener implements HSSFListener {
    private XlsReadContext xlsReadContext;
    private static final Map<Short, XlsRecordHandler> XLS_RECORD_HANDLER_MAP = new HashMap<Short, XlsRecordHandler>();

    static {
        XLS_RECORD_HANDLER_MAP.put(BOFRecord.sid, new BofRecordHandler());
        XLS_RECORD_HANDLER_MAP.put(BoundSheetRecord.sid, new BoundSheetRecordHandler());
    }

    public XlsListSheetListener(XlsReadContext xlsReadContext) {
        this.xlsReadContext = xlsReadContext;
        xlsReadContext.xlsReadWorkbookHolder().setNeedReadSheet(Boolean.FALSE);
    }

    @Override
    public void processRecord(Record record) {
        XlsRecordHandler handler = XLS_RECORD_HANDLER_MAP.get(record.getSid());
        if (handler == null) {
            return;
        }
        handler.processRecord(xlsReadContext, record);
    }

    public void execute() {
        MissingRecordAwareHSSFListener listener = new MissingRecordAwareHSSFListener(this);
        HSSFListener formatListener = new FormatTrackingHSSFListener(listener);
        HSSFEventFactory factory = new HSSFEventFactory();
        HSSFRequest request = new HSSFRequest();
        EventWorkbookBuilder.SheetRecordCollectingListener workbookBuildingListener =
                new EventWorkbookBuilder.SheetRecordCollectingListener(formatListener);
        request.addListenerForAllRecords(workbookBuildingListener);
        try {
            factory.processWorkbookEvents(request, xlsReadContext.xlsReadWorkbookHolder().getPoifsFileSystem());
        } catch (IOException e) {
            throw new ExcelAnalysisException(e);
        }
    }
}

