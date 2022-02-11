package com.example.mybatisgen.excel.analysis.v03.handlers;

import org.apache.poi.hssf.record.HyperlinkRecord;
import org.apache.poi.hssf.record.Record;

import com.example.mybatisgen.excel.analysis.v03.IgnorableXlsRecordHandler;
import com.example.mybatisgen.excel.context.xls.XlsReadContext;
import com.example.mybatisgen.excel.enums.CellExtraTypeEnum;
import com.example.mybatisgen.excel.metadata.CellExtra;

/**
 * Record handler
 *
 * @author Dan Zheng
 */
public class HyperlinkRecordHandler extends AbstractXlsRecordHandler implements IgnorableXlsRecordHandler {
    @Override
    public boolean support(XlsReadContext xlsReadContext, Record record) {
        return xlsReadContext.readWorkbookHolder().getExtraReadSet().contains(CellExtraTypeEnum.HYPERLINK);
    }

    @Override
    public void processRecord(XlsReadContext xlsReadContext, Record record) {
        HyperlinkRecord hr = (HyperlinkRecord)record;
        CellExtra cellExtra = new CellExtra(CellExtraTypeEnum.HYPERLINK, hr.getAddress(), hr.getFirstRow(),
                hr.getLastRow(), hr.getFirstColumn(), hr.getLastColumn());
        xlsReadContext.xlsReadSheetHolder().setCellExtra(cellExtra);
        xlsReadContext.analysisEventProcessor().extra(xlsReadContext);
    }
}
