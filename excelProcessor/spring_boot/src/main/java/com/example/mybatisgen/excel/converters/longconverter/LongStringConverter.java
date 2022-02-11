package com.example.mybatisgen.excel.converters.longconverter;

import com.example.mybatisgen.excel.converters.Converter;
import com.example.mybatisgen.excel.enums.CellDataTypeEnum;
import com.example.mybatisgen.excel.metadata.CellData;
import com.example.mybatisgen.excel.metadata.GlobalConfiguration;
import com.example.mybatisgen.excel.metadata.property.ExcelContentProperty;
import com.example.mybatisgen.excel.util.NumberUtils;

import java.text.ParseException;

/**
 * Long and string converter
 *
 * @author Jiaju Zhuang
 */
public class LongStringConverter implements Converter<Long> {

    @Override
    public Class supportJavaTypeKey() {
        return Long.class;
    }

    @Override
    public CellDataTypeEnum supportExcelTypeKey() {
        return CellDataTypeEnum.STRING;
    }

    @Override
    public Long convertToJavaData(CellData cellData, ExcelContentProperty contentProperty,
                                  GlobalConfiguration globalConfiguration) throws ParseException {
        return NumberUtils.parseLong(cellData.getStringValue(), contentProperty);
    }

    @Override
    public CellData convertToExcelData(Long value, ExcelContentProperty contentProperty,
                                       GlobalConfiguration globalConfiguration) {
        return NumberUtils.formatToCellData(value, contentProperty);
    }
}
