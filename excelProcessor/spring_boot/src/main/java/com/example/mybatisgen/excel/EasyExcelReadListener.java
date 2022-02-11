package com.example.mybatisgen.excel;


import com.example.mybatisgen.entity.Easyexcelmodel;
import com.example.mybatisgen.excel.context.AnalysisContext;
import com.example.mybatisgen.excel.event.AnalysisEventListener;
import com.example.mybatisgen.mapper.EasyexcelmodelMapper;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.ArrayList;
import java.util.List;

@Slf4j
public class EasyExcelReadListener extends AnalysisEventListener<Easyexcelmodel> {

    @Autowired
    private EasyexcelmodelMapper easyExcelMapper;

    private List<Easyexcelmodel> easyExcelModels = new ArrayList<>();

//    private static final int BATCH_COUNT = 5;

    public EasyExcelReadListener(EasyexcelmodelMapper easyExcelMapper) {
        this.easyExcelMapper = easyExcelMapper;
    }

    @Override
    public void invoke(Easyexcelmodel easyExcel, AnalysisContext analysisContext) {
        log.info("开始读取文章：{}", easyExcel.toString());
        easyExcelModels.add(easyExcel);
//        if (easyExcelModels.size() >= BATCH_COUNT) {
//            saveData();
//            easyExcelModels.clear();
//        }
    }

    @Override
    public void doAfterAllAnalysed(AnalysisContext analysisContext) {
        log.info("进入到：doAfterAllAnalysed  方法中");
        easyExcelModels.forEach(easyExcelModel -> {
            easyExcelMapper.insert(easyExcelModel);
        });
        saveData();
    }

    /**
     * 加上存储数据库
     */
    private void saveData() {
        log.info("存储数据库成功！");
    }
}