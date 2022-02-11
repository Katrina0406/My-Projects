package com.example.mybatisgen.controller;

import com.example.mybatisgen.entity.Easyexcelmodel;
import com.example.mybatisgen.entity.NewModel;
import com.example.mybatisgen.excel.EasyExcel;
import com.example.mybatisgen.excel.EasyExcelReadListener;
import com.example.mybatisgen.excel.ExcelWriter;
import com.example.mybatisgen.excel.write.metadata.WriteSheet;
import com.example.mybatisgen.excel.write.metadata.fill.FillConfig;
import com.example.mybatisgen.mapper.EasyexcelmodelMapper;
import com.example.mybatisgen.service.IEasyExcelService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestController;

import javax.servlet.http.HttpServletResponse;
import java.io.*;
import java.net.URLEncoder;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/easyExcel")
public class EasyExcelController {
    @Autowired
    private IEasyExcelService iEasyExcelService;

    @Autowired
    private EasyexcelmodelMapper easyExcelMapper;

    @GetMapping("/template")
    public void template(HttpServletResponse response) throws IOException {
        response.setContentType("application/vnd.ms-excel");
        response.setCharacterEncoding("utf-8");
        String fileName = URLEncoder.encode("数据上传模板", "UTF-8");
        response.setHeader("Content-disposition", "attachment;filename=" + fileName + ".xlsx");
        EasyExcel.write(response.getOutputStream(), Easyexcelmodel.class ).sheet("数据上传模板").doWrite(new ArrayList<Easyexcelmodel>());
    }
    @GetMapping("/template1")
    public String  template1() throws IOException {
           return "hello world" ;
    }

//    @RequestMapping("/upload")
//    @ResponseBody
//    public String upload(MultipartFile file) throws IOException {
//        EasyExcel.read(file.getInputStream(),EasyExcelModel.class , new EasyExcelReadListener(easyExcelMapper)).sheet().doRead();
//        return "success";
//    }

    @RequestMapping("/upload")
    @ResponseBody
    public String upload() throws IOException {
        File file = new File("src/main/resources/sample.xlsx");
        InputStream in = new FileInputStream(file);
        EasyExcel.read(in, Easyexcelmodel.class , new EasyExcelReadListener(easyExcelMapper)).sheet().doRead();
        return "success";
    }

    @GetMapping("/download")
    public void download(HttpServletResponse response) throws IOException {
        response.setContentType("application/vnd.ms-excel");
        response.setCharacterEncoding("utf-8");
        String fileName = URLEncoder.encode("数据表格下载", "UTF-8");
        response.setHeader("Content-disposition", "attachment;filename=" + fileName + ".xlsx");
        EasyExcel.write(response.getOutputStream(), Easyexcelmodel.class).sheet("数据表格").doWrite(iEasyExcelService.list());
    }


    @RequestMapping("/export")
    public String exporExcel(HttpServletResponse response) throws IOException {
        OutputStream outputStream = response.getOutputStream();
        response.setHeader("Content-disposition", "attachment; filename=" + "catagory.xlsx");
        response.setContentType("application/msexcel;charset=UTF-8");//设置类型
        response.setHeader("Pragma", "No-cache");//设置头
        response.setHeader("Cache-Control", "no-cache");//设置头
        response.setDateHeader("Expires", 0);//设置日期头
        //模板的存放地址
        String templatePath = "/Users/katrina/Downloads/model.xlsx";
        ExcelWriter excelWriter = EasyExcel.write(outputStream).withTemplate(new File(templatePath)).build();
        WriteSheet writeSheet = EasyExcel.writerSheet().build();
        List<NewModel> list =new ArrayList<NewModel>();
        //按model在List中的顺序填写，可填写多组数据
        NewModel nm = new NewModel();
        nm.setColor("green");
        nm.setCommodity("apple pie");
        nm.setNumber("27");
        nm.setTravel("2000082420020517");
        nm.setCompany("baofengzhouyu");
        nm.setRemark("love forever");
        //填充两行list
        list.add(nm);
        list.add(nm);
        FillConfig fillConfig = FillConfig.builder().forceNewRow(Boolean.TRUE).build();
        excelWriter.fill(list, fillConfig, writeSheet);
        //填充普通变量
        Map<String, Object> map = new HashMap<String, Object>();
        map.put("bussinessRequest", "今日头条");
        map.put("linkman", "周六");
        map.put("linkphone", "188997766");
        map.put("orderdate", "20201207");
        map.put("leaddate", "20210527");
        map.put("entrct", "获取最新日常");
        map.put("customer", "2");
        excelWriter.fill(map, writeSheet);
        excelWriter.finish();
        outputStream.flush();
        response.getOutputStream().close();
        return "success";
    }

//    @Override
//    public void exportInfo(List<CustomerInfo> customerDealerInfo, HttpServletResponse response) throws IOException {
//        OutputStream out = null;
//        BufferedOutputStream bos = null;
//        try {
//            String templateFileName = FileUtil.getPath() + "templates" + File.separator + "模板.xls";
//
//            response.setContentType("application/vnd.ms-excel");
//            response.setCharacterEncoding("utf-8");
//            String fileName = URLEncoder.encode("下载后的名称.xls", "utf-8");
//            response.setHeader("Content-disposition", "attachment; filename=" + new String(fileName.getBytes("UTF-8"), "ISO-8859-1"));
//
//            out = response.getOutputStream();
//            bos = new BufferedOutputStream(out);
//
//            //读取Excel
//            ExcelWriter excelWriter = EasyExcel.write(bos).withTemplate(templateFileName).build();
//            WriteSheet writeSheet = EasyExcel.writerSheet().build();
//
//            //customerDealerInfo 是我查询并需导出的数据，并且里面的字段和excel需要导出的字段对应
//            // 直接写入Excel数据
//            excelWriter.fill(customerDealerInfo, writeSheet);
//            excelWriter.finish();
//            bos.flush();
//
//        } catch (Exception e) {
//            // 重置response
//            response.reset();
//            response.setContentType("application/json");
//            response.setCharacterEncoding("utf-8");
//            Map<String, String> map = new HashMap<String, String>(16);
//            map.put("status", "failure");
//            map.put("message", "下载文件失败" + e.getMessage());
//            response.getWriter().println(JSON.toJSONString(map));
//        }
//    }

}