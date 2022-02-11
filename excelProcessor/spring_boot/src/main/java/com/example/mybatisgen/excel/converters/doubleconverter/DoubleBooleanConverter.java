package com.example.mybatisgen.excel.converters.doubleconverter;

import com.example.mybatisgen.excel.converters.Converter;
import com.example.mybatisgen.excel.enums.CellDataTypeEnum;
import com.example.mybatisgen.excel.metadata.CellData;
import com.example.mybatisgen.excel.metadata.GlobalConfiguration;
import com.example.mybatisgen.excel.metadata.property.ExcelContentProperty;

/**
 * Double and boolean converter
 *
 * @author Jiaju Zhuang
 */
public class DoubleBooleanConverter implements Converter<Double> {
    private static final Double ONE = 1.0;
    private static final Double ZERO = 0.0;

    @Override
    public Class supportJavaTypeKey() {
        return Double.class;
    }

    @Override
    public CellDataTypeEnum supportExcelTypeKey() {
        return CellDataTypeEnum.BOOLEAN;
    }

    @Override
    public Double convertToJavaData(CellData cellData, ExcelContentProperty contentProperty,
                                    GlobalConfiguration globalConfiguration) {
        if (cellData.getBooleanValue()) {
            return ONE;
        }
        return ZERO;
    }

    @Override
    public CellData convertToExcelData(Double value, ExcelContentProperty contentProperty,
                                       GlobalConfiguration globalConfiguration) {
        if (ONE.equals(value)) {
            return new CellData(Boolean.TRUE);
        }
        return new CellData(Boolean.FALSE);
    }

}

