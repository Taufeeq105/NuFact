package org.example;

import com.google.gson.JsonArray;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;

import java.io.IOException;
import java.net.URI;
import java.net.URLEncoder;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class googlesearchapi {

    private static final String CUSTOM_SEARCH_API_ENDPOINT = "https://www.googleapis.com/customsearch/v1";
    private static final String API_KEY = "ADD_YOUR_KEY";  //
    private static final String CX = "ADD_YOUR_KEY";

    public List<String> getSearchResults(String query) {
        List<String> resultUrls = new ArrayList<>();

        try {
            String encodedQuery = URLEncoder.encode(query, StandardCharsets.UTF_8);
//            String searchUrl = String.format("%s?key=%s&cx=%s&q=%s&num=%d", CUSTOM_SEARCH_API_ENDPOINT, API_KEY, CX, encodedQuery, 20);
            String searchUrl = String.format("%s?key=%s&cx=%s&q=%s", CUSTOM_SEARCH_API_ENDPOINT, API_KEY, CX, encodedQuery);
            HttpClient client = HttpClient.newHttpClient();
            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create(searchUrl))
                    .build();

            HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());

            if (response.statusCode() == 200) {
                processResponse(response.body(), resultUrls);
            } else {
                handleErrorResponse(response.statusCode());
            }
        } catch (IOException | InterruptedException e) {
            handleException(e);
        }

        return resultUrls;
    }

    private void processResponse(String responseBody, List<String> resultUrls) {
        JsonParser parser = new JsonParser();
        JsonObject jsonResponse = parser.parse(responseBody).getAsJsonObject();

        // Check if the response contains items
        if (jsonResponse.has("items")) {
            JsonArray items = jsonResponse.getAsJsonArray("items");

            for (int i = 0; i < items.size(); i++) {
                JsonObject item = items.get(i).getAsJsonObject();
                String link = item.has("link") ? item.get("link").getAsString() : null;

                if (link != null) {
                    resultUrls.add(link);
                }
            }
        }
    }

    private void handleErrorResponse(int responseCode) {
        System.out.println("Error in HTTP request, response code: " + responseCode);
    }
    public static double calculateTermRatio(String webpageContent, List<String> termList) {
        // Step 1: Tokenize the web page content into words
        List<String> contentWords = Arrays.asList(webpageContent.split("\\s+"));

        // Step 2: Count how many terms from the list appear in the content
        long appearingTermCount = termList.stream()
                .filter(term -> contentWords.stream().anyMatch(word -> word.equalsIgnoreCase(term)))
                .count();

        // Step 3: Calculate the ratio
        double totalTermCount = termList.size();
        double termRatio = appearingTermCount / totalTermCount;

        return termRatio;
    }
    private void handleException(Exception e) {
        // Log or throw a custom exception
        e.printStackTrace();
    }
}
