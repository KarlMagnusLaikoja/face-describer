package com.facedescriber;

import com.facedescriber.constants.BackendError;
import com.facedescriber.validation.PythonException;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;

@SpringBootApplication
public class FaceDescriberApplication {

	public static void main(String[] args) {
		setup();
		SpringApplication.run(FaceDescriberApplication.class, args);
	}
	public static void setup(){
		ProcessBuilder processBuilder = new ProcessBuilder("/usr/bin/env", "bash", "setup.sh");
		processBuilder.directory(new File("src/main/python"));
		processBuilder.redirectErrorStream(true);
		try {
			processBuilder.start();
		} catch (IOException e) {
			throw new RuntimeException("Failed to setup python virtual environment: "+e);
		}
	}

}
