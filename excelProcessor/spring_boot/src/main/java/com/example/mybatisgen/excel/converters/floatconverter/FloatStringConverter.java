package com.example.mybatisgen.excel.converters.floatconverter;

import com.example.mybatisgen.excel.converters.Converter;
import com.example.mybatisgen.excel.enums.CellDataTypeEnum;
import com.example.mybatisgen.excel.metadata.CellData;
import com.example.mybatisgen.excel.metadata.GlobalConfiguration;
import com.example.mybatisgen.excel.metadata.property.ExcelContentProperty;
import com.example.mybatisgen.excel.util.NumberUtils;

import java.text.ParseException;

/**
 * Float and string converter
 *
 * @author Jiaju Zhuang
 */
public class FloatStringConverter implements Converter<Float> {

    @Override
    public Class supportJavaTypeKey() {
        return Float.class;
    }

    @Override
    public CellDataTypeEnum supportExcelTypeKey() {
        return CellDataTypeEnum.STRING;
    }

    @Override
    public Float convertToJavaData(CellData cellData, ExcelContentProperty contentProperty,
                                   GlobalConfiguration globalConfiguration) throws ParseException {
        return NumberUtils.parseFloat(cellData.getStringValue(), contentProperty);
    }

    @Override
    public CellData convertToExcelData(Float value, ExcelContentProperty contentProperty,
                                       GlobalConfiguration globalConfiguration) {
        return NumberUtils.formatToCellData(value, contentProperty);
    }
}
