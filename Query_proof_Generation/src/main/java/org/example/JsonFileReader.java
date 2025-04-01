package org.example;

import com.fasterxml.jackson.databind.ObjectMapper;

import java.io.File;
import java.io.IOException;
import java.util.Map;

public class JsonFileReader {

    private final Map<String, Object> jsonMap;

    public JsonFileReader(String filePath) {
        this.jsonMap = readJsonFile(filePath);
    }

    private Map<String, Object> readJsonFile(String filePath) {
        try {
            // Create ObjectMapper
            ObjectMapper objectMapper = new ObjectMapper();

            // Read JSON file and convert it to a Map
            return objectMapper.readValue(new File(filePath), Map.class);
        } catch (IOException e) {
            e.printStackTrace();
            return null;
        }
    }

    public Object getValueForKey(String key) {
        if (jsonMap != null && jsonMap.containsKey(key)) {
            return jsonMap.get(key);
        } else {
            System.out.println("Key not found: " + key);
            return null;
        }
    }

}
