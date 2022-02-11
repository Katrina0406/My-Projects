package com.example.mybatisgen.excel.converters.floatconverter;

import com.example.mybatisgen.excel.converters.Converter;
import com.example.mybatisgen.excel.enums.CellDataTypeEnum;
import com.example.mybatisgen.excel.metadata.CellData;
import com.example.mybatisgen.excel.metadata.GlobalConfiguration;
import com.example.mybatisgen.excel.metadata.property.ExcelContentProperty;

import java.math.BigDecimal;

/**
 * Float and number converter
 *
 * @author Jiaju Zhuang
 */
public class FloatNumberConverter implements Converter<Float> {

    @Override
    public Class supportJavaTypeKey() {
        return Float.class;
    }

    @Override
    public CellDataTypeEnum supportExcelTypeKey() {
        return CellDataTypeEnum.NUMBER;
    }

    @Override
    public Float convertToJavaData(CellData cellData, ExcelContentProperty contentProperty,
                                   GlobalConfiguration globalConfiguration) {
        return cellData.getNumberValue().floatValue();
    }

    @Override
    public CellData convertToExcelData(Float value, ExcelContentProperty contentProperty,
                                       GlobalConfiguration globalConfiguration) {
        return new CellData(new BigDecimal(Float.toString(value)));
    }

}
