package com.facedescriber;


import com.facedescriber.constants.BackendError;
import com.facedescriber.validation.PythonException;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;

@SpringBootApplication
public class FaceDescriberApplication {

	private static Logger logger = LogManager.getLogger();

	public static void main(String[] args) {
		SpringApplication.run(FaceDescriberApplication.class, args);
	}


}
