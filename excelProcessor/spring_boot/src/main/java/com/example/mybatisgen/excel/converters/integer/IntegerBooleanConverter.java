package com.example.mybatisgen.excel.converters.integer;

import com.example.mybatisgen.excel.converters.Converter;
import com.example.mybatisgen.excel.enums.CellDataTypeEnum;
import com.example.mybatisgen.excel.metadata.CellData;
import com.example.mybatisgen.excel.metadata.GlobalConfiguration;
import com.example.mybatisgen.excel.metadata.property.ExcelContentProperty;

/**
 * Integer and boolean converter
 *
 * @author Jiaju Zhuang
 */
public class IntegerBooleanConverter implements Converter<Integer> {
    private static final Integer ONE = 1;
    private static final Integer ZERO = 0;

    @Override
    public Class supportJavaTypeKey() {
        return Integer.class;
    }

    @Override
    public CellDataTypeEnum supportExcelTypeKey() {
        return CellDataTypeEnum.BOOLEAN;
    }

    @Override
    public Integer convertToJavaData(CellData cellData, ExcelContentProperty contentProperty,
                                     GlobalConfiguration globalConfiguration) {
        if (cellData.getBooleanValue()) {
            return ONE;
        }
        return ZERO;
    }

    @Override
    public CellData convertToExcelData(Integer value, ExcelContentProperty contentProperty,
                                       GlobalConfiguration globalConfiguration) {
        if (ONE.equals(value)) {
            return new CellData(Boolean.TRUE);
        }
        return new CellData(Boolean.FALSE);
    }

}
