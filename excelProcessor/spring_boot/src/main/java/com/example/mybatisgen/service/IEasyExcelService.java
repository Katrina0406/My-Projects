package com.example.mybatisgen.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@Service
public class IEasyExcelService {
    @Autowired
    public List list(){
        List<Integer> result = new ArrayList<Integer>();
        return result;
    }
}
