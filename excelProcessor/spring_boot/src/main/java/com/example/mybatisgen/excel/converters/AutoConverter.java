package com.example.mybatisgen.excel.converters;

import com.example.mybatisgen.excel.enums.CellDataTypeEnum;
import com.example.mybatisgen.excel.metadata.CellData;
import com.example.mybatisgen.excel.metadata.GlobalConfiguration;
import com.example.mybatisgen.excel.metadata.property.ExcelContentProperty;

/**
 * An empty converter.It's automatically converted by type.
 *
 * @author Jiaju Zhuang
 */
public class AutoConverter implements Converter {

    @Override
    public Class supportJavaTypeKey() {
        return null;
    }

    @Override
    public CellDataTypeEnum supportExcelTypeKey() {
        return null;
    }

    @Override
    public Object convertToJavaData(CellData cellData, ExcelContentProperty contentProperty,
                                    GlobalConfiguration globalConfiguration) {
        return null;
    }

    @Override
    public CellData convertToExcelData(Object value, ExcelContentProperty contentProperty,
                                       GlobalConfiguration globalConfiguration) {
        return null;
    }
}

