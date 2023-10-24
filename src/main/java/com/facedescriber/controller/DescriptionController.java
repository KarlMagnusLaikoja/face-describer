package com.facedescriber.controller;

import com.facedescriber.logic.DescriptionLogic;
import jakarta.servlet.http.HttpServletResponse;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class DescriptionController {
    private static Logger logger = LogManager.getLogger();
    @Autowired
    DescriptionLogic logic;
    @PostMapping(value = "/describe", consumes = MediaType.APPLICATION_JSON_VALUE)
    @CrossOrigin()
    public ResponseEntity<String> describeEndpoint(@RequestBody String data){
        logger.info("IN: "+data);
        logic.setData(data);
        String result = logic.execute();
        logger.info("OUT: "+result);

        HttpHeaders responseHeaders = new HttpHeaders();
        responseHeaders.set("Content-type", "application/json;charset=UTF-8");
        return new ResponseEntity<String>(result, responseHeaders, HttpStatus.OK);
    }
}
