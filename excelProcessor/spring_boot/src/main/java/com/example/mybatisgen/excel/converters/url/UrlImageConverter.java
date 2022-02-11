package com.example.mybatisgen.excel.converters.url;

import com.example.mybatisgen.excel.converters.Converter;
import com.example.mybatisgen.excel.enums.CellDataTypeEnum;
import com.example.mybatisgen.excel.metadata.CellData;
import com.example.mybatisgen.excel.metadata.GlobalConfiguration;
import com.example.mybatisgen.excel.metadata.property.ExcelContentProperty;
import com.example.mybatisgen.excel.util.IoUtils;

import java.io.IOException;
import java.io.InputStream;
import java.net.URL;

/**
 * Url and image converter
 *
 * @since 2.1.1
 * @author Jiaju Zhuang
 */
public class UrlImageConverter implements Converter<URL> {
    @Override
    public Class supportJavaTypeKey() {
        return URL.class;
    }

    @Override
    public CellDataTypeEnum supportExcelTypeKey() {
        return CellDataTypeEnum.IMAGE;
    }

    @Override
    public URL convertToJavaData(CellData cellData, ExcelContentProperty contentProperty,
                                 GlobalConfiguration globalConfiguration) {
        throw new UnsupportedOperationException("Cannot convert images to url.");
    }

    @Override
    public CellData convertToExcelData(URL value, ExcelContentProperty contentProperty,
                                       GlobalConfiguration globalConfiguration) throws IOException {
        InputStream inputStream = null;
        try {
            inputStream = value.openStream();
            byte[] bytes = IoUtils.toByteArray(inputStream);
            return new CellData(bytes);
        } finally {
            if (inputStream != null) {
                inputStream.close();
            }
        }
    }

}
