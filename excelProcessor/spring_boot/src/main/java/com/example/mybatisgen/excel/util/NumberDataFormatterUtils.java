package com.example.mybatisgen.excel.util;

import java.math.BigDecimal;

import com.example.mybatisgen.excel.metadata.format.DataFormatter;
import com.example.mybatisgen.excel.metadata.GlobalConfiguration;

/**
 * Convert number data, including date.
 *
 * @author Jiaju Zhuang
 **/
public class NumberDataFormatterUtils {

    /**
     * Cache DataFormatter.
     */
    private static final ThreadLocal<DataFormatter> DATA_FORMATTER_THREAD_LOCAL = new ThreadLocal<DataFormatter>();

    /**
     * Format number data.
     *
     * @param data
     * @param dataFormat          Not null.
     * @param dataFormatString
     * @param globalConfiguration
     * @return
     */
    public static String format(BigDecimal data, Integer dataFormat, String dataFormatString,
                                GlobalConfiguration globalConfiguration) {
        DataFormatter dataFormatter = DATA_FORMATTER_THREAD_LOCAL.get();
        if (dataFormatter == null) {
            dataFormatter = new DataFormatter(globalConfiguration);
            DATA_FORMATTER_THREAD_LOCAL.set(dataFormatter);
        }
        return dataFormatter.format(data, dataFormat, dataFormatString);

    }

    public static void removeThreadLocalCache() {
        DATA_FORMATTER_THREAD_LOCAL.remove();
    }
}
