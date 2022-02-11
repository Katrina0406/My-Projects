package com.example.mybatisgen.excel.converters.byteconverter;

import com.example.mybatisgen.excel.converters.Converter;
import com.example.mybatisgen.excel.enums.CellDataTypeEnum;
import com.example.mybatisgen.excel.metadata.CellData;
import com.example.mybatisgen.excel.metadata.GlobalConfiguration;
import com.example.mybatisgen.excel.metadata.property.ExcelContentProperty;
import com.example.mybatisgen.excel.util.NumberUtils;

import java.text.ParseException;

/**
 * Byte and string converter
 *
 * @author Jiaju Zhuang
 */
public class ByteStringConverter implements Converter<Byte> {

    @Override
    public Class supportJavaTypeKey() {
        return Byte.class;
    }

    @Override
    public CellDataTypeEnum supportExcelTypeKey() {
        return CellDataTypeEnum.STRING;
    }

    @Override
    public Byte convertToJavaData(CellData cellData, ExcelContentProperty contentProperty,
                                  GlobalConfiguration globalConfiguration) throws ParseException {
        return NumberUtils.parseByte(cellData.getStringValue(), contentProperty);
    }

    @Override
    public CellData convertToExcelData(Byte value, ExcelContentProperty contentProperty,
                                       GlobalConfiguration globalConfiguration) {
        return NumberUtils.formatToCellData(value, contentProperty);
    }

}
