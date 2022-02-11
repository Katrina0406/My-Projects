package com.example.mybatisgen.excel.analysis.v07.handlers;

import java.math.BigDecimal;

import com.example.mybatisgen.excel.context.xlsx.XlsxReadContext;
import com.example.mybatisgen.excel.enums.CellDataTypeEnum;
import com.example.mybatisgen.excel.metadata.CellData;
import com.example.mybatisgen.excel.read.metadata.holder.xlsx.XlsxReadSheetHolder;
import com.example.mybatisgen.excel.util.BooleanUtils;
import com.example.mybatisgen.excel.util.StringUtils;

/**
 * Cell Value Handler
 *
 * @author jipengfei
 */
public abstract class AbstractCellValueTagHandler extends AbstractXlsxTagHandler {

    @Override
    public void endElement(XlsxReadContext xlsxReadContext, String name) {
        XlsxReadSheetHolder xlsxReadSheetHolder = xlsxReadContext.xlsxReadSheetHolder();
        CellData tempCellData = xlsxReadSheetHolder.getTempCellData();
        StringBuilder tempData = xlsxReadSheetHolder.getTempData();
        String tempDataString = tempData.toString();
        CellDataTypeEnum oldType = tempCellData.getType();
        switch (oldType) {
            case DIRECT_STRING:
            case STRING:
            case ERROR:
                tempCellData.setStringValue(tempData.toString());
                break;
            case BOOLEAN:
                if(StringUtils.isEmpty(tempDataString)){
                    tempCellData.setType(CellDataTypeEnum.EMPTY);
                    break;
                }
                tempCellData.setBooleanValue(BooleanUtils.valueOf(tempData.toString()));
                break;
            case NUMBER:
            case EMPTY:
                if(StringUtils.isEmpty(tempDataString)){
                    tempCellData.setType(CellDataTypeEnum.EMPTY);
                    break;
                }
                tempCellData.setType(CellDataTypeEnum.NUMBER);
                tempCellData.setNumberValue(BigDecimal.valueOf(Double.parseDouble(tempDataString)));
                break;
            default:
                throw new IllegalStateException("Cannot set values now");
        }

        // set string value
        setStringValue(xlsxReadContext);

        if (tempCellData.getStringValue() != null
                && xlsxReadContext.currentReadHolder().globalConfiguration().getAutoTrim()) {
            tempCellData.setStringValue(tempCellData.getStringValue());
        }

        tempCellData.checkEmpty();
        xlsxReadSheetHolder.getCellMap().put(xlsxReadSheetHolder.getColumnIndex(), tempCellData);
    }

    @Override
    public void characters(XlsxReadContext xlsxReadContext, char[] ch, int start, int length) {
        xlsxReadContext.xlsxReadSheetHolder().getTempData().append(ch, start, length);
    }

    /**
     * Set string value.
     *
     * @param xlsxReadContext
     */
    protected abstract void setStringValue(XlsxReadContext xlsxReadContext);

}