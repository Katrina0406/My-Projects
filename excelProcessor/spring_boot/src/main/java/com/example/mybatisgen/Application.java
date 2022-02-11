package com.example.mybatisgen;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;


//(exclude= {DataSourceAutoConfiguration.class})
@SpringBootApplication
//配置扫描mapper文件，不必每个mapper文件都添加@mapper注解
@MapperScan("com.example.mybatisgen.mapper")
public class Application {

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }

}
