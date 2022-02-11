package com.example.mybatisgen.excel.analysis.v07.handlers;

import org.xml.sax.Attributes;

import com.example.mybatisgen.excel.constant.ExcelXmlConstants;
import com.example.mybatisgen.excel.context.xlsx.XlsxReadContext;

/**
 * Cell Handler
 *
 * @author jipengfei
 */
public class CountTagHandler extends AbstractXlsxTagHandler {

    @Override
    public void startElement(XlsxReadContext xlsxReadContext, String name, Attributes attributes) {
        String d = attributes.getValue(ExcelXmlConstants.ATTRIBUTE_REF);
        String totalStr = d.substring(d.indexOf(":") + 1, d.length());
        String c = totalStr.toUpperCase().replaceAll("[A-Z]", "");
        xlsxReadContext.readSheetHolder().setApproximateTotalRowNumber(Integer.parseInt(c));
    }

}
