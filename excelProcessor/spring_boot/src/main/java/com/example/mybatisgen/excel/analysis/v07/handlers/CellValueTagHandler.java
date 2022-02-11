package com.example.mybatisgen.excel.analysis.v07.handlers;

import com.example.mybatisgen.excel.context.xlsx.XlsxReadContext;
import com.example.mybatisgen.excel.enums.CellDataTypeEnum;
import com.example.mybatisgen.excel.metadata.CellData;
import com.example.mybatisgen.excel.util.StringUtils;

/**
 * Cell Value Handler
 *
 * @author jipengfei
 */
public class CellValueTagHandler extends AbstractCellValueTagHandler {

    @Override
    protected void setStringValue(XlsxReadContext xlsxReadContext) {
        // Have to go "sharedStrings.xml" and get it
        CellData tempCellData = xlsxReadContext.xlsxReadSheetHolder().getTempCellData();
        switch (tempCellData.getType()) {
            case STRING:
                // In some cases, although cell type is a string, it may be an empty tag
                if(StringUtils.isEmpty(tempCellData.getStringValue())){
                    break;
                }
                String stringValue = xlsxReadContext.readWorkbookHolder().getReadCache()
                        .get(Integer.valueOf(tempCellData.getStringValue()));
                if (stringValue != null && xlsxReadContext.currentReadHolder().globalConfiguration().getAutoTrim()) {
                    stringValue = stringValue.trim();
                }
                tempCellData.setStringValue(stringValue);
                break;
            case DIRECT_STRING:
                tempCellData.setType(CellDataTypeEnum.STRING);
                break;
            default:
        }
    }

}
