package com.facedescriber.controller;

import com.facedescriber.logic.DescriptionLogic;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class PostController {
    private static Logger logger = LogManager.getLogger();
    @Autowired
    DescriptionLogic logic;
    @PostMapping(value = "/describe", consumes = MediaType.APPLICATION_JSON_VALUE)
    public String describeEndpoint(@RequestBody String data){
        logger.info("IN: "+data);
        logic.setData(data);
        String response = logic.execute();
        logger.info("OUT: "+response);
        return response;
    }
}
