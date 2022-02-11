package com.example.mybatisgen.excel.converters.byteconverter;

import com.example.mybatisgen.excel.converters.Converter;
import com.example.mybatisgen.excel.enums.CellDataTypeEnum;
import com.example.mybatisgen.excel.metadata.CellData;
import com.example.mybatisgen.excel.metadata.GlobalConfiguration;
import com.example.mybatisgen.excel.metadata.property.ExcelContentProperty;

/**
 * Byte and boolean converter
 *
 * @author Jiaju Zhuang
 */
public class ByteBooleanConverter implements Converter<Byte> {
    private static final Byte ONE = (byte)1;
    private static final Byte ZERO = (byte)0;

    @Override
    public Class supportJavaTypeKey() {
        return Byte.class;
    }

    @Override
    public CellDataTypeEnum supportExcelTypeKey() {
        return CellDataTypeEnum.BOOLEAN;
    }

    @Override
    public Byte convertToJavaData(CellData cellData, ExcelContentProperty contentProperty,
                                  GlobalConfiguration globalConfiguration) {
        if (cellData.getBooleanValue()) {
            return ONE;
        }
        return ZERO;
    }

    @Override
    public CellData convertToExcelData(Byte value, ExcelContentProperty contentProperty,
                                       GlobalConfiguration globalConfiguration) {
        if (ONE.equals(value)) {
            return new CellData(Boolean.TRUE);
        }
        return new CellData(Boolean.FALSE);
    }

}