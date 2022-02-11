package com.example.mybatisgen.excel.converters.doubleconverter;

import com.example.mybatisgen.excel.converters.Converter;
import com.example.mybatisgen.excel.enums.CellDataTypeEnum;
import com.example.mybatisgen.excel.metadata.CellData;
import com.example.mybatisgen.excel.metadata.GlobalConfiguration;
import com.example.mybatisgen.excel.metadata.property.ExcelContentProperty;

import java.math.BigDecimal;

/**
 * Double and number converter
 *
 * @author Jiaju Zhuang
 */
public class DoubleNumberConverter implements Converter<Double> {

    @Override
    public Class supportJavaTypeKey() {
        return Double.class;
    }

    @Override
    public CellDataTypeEnum supportExcelTypeKey() {
        return CellDataTypeEnum.NUMBER;
    }

    @Override
    public Double convertToJavaData(CellData cellData, ExcelContentProperty contentProperty,
                                    GlobalConfiguration globalConfiguration) {
        return cellData.getNumberValue().doubleValue();
    }

    @Override
    public CellData convertToExcelData(Double value, ExcelContentProperty contentProperty,
                                       GlobalConfiguration globalConfiguration) {
        return new CellData(BigDecimal.valueOf(value));
    }

}
