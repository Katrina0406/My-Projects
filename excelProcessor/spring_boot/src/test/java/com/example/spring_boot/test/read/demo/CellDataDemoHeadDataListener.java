package com.example.spring_boot.test.read.demo;

import com.example.mybatisgen.excel.context.AnalysisContext;
import com.example.mybatisgen.excel.event.AnalysisEventListener;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.ArrayList;
import java.util.List;

/**
 * 读取头
 *
 * @author Jiaju Zhuang
 */
public class CellDataDemoHeadDataListener extends AnalysisEventListener<CellDataReadDemoData> {
    private static final Logger LOGGER = LoggerFactory.getLogger(CellDataDemoHeadDataListener.class);
    /**
     * 每隔5条存储数据库，实际使用中可以3000条，然后清理list ，方便内存回收
     */
    private static final int BATCH_COUNT = 5;
    List<CellDataReadDemoData> list = new ArrayList<CellDataReadDemoData>();

    @Override
    public void invoke(CellDataReadDemoData data, AnalysisContext context) {
//        LOGGER.info("解析到一条数据:{}", JSON.toJSONString(data));
        System.out.print(data);
        if (list.size() >= BATCH_COUNT) {
            saveData();
            list.clear();
        }
    }

    @Override
    public void doAfterAllAnalysed(AnalysisContext context) {
        saveData();
        LOGGER.info("所有数据解析完成！");
    }

    /**
     * 加上存储数据库
     */
    private void saveData() {
        LOGGER.info("{}条数据，开始存储数据库！", list.size());
        LOGGER.info("存储数据库成功！");
    }
}
