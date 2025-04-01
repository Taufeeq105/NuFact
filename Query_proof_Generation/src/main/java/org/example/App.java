package org.example;
import java.io.*;
import java.util.ArrayList;
import java.util.stream.Collectors;
//import org.apache.lucene.analysis.Analyzer;
//import org.apache.lucene.analysis.TokenStream;
//import org.apache.lucene.analysis.core.SimpleAnalyzer;
//import org.apache.lucene.analysis.tokenattributes.CharTermAttribute;
import org.apache.commons.io.IOUtils;
import org.json.JSONArray;
import org.json.JSONObject;
import org.jsoup.Connection;
import org.jsoup.HttpStatusException;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
//import org.json.JSONTokener;
//import org.apache.lucene.analysis.CharArraySet;
//import org.apache.lucene.analysis.en.EnglishAnalyzer;
import java.io.FileInputStream;
import java.util.List;
//import java.util.Set;
//import java.util.Iterator;


public class App {

//    public static void writeListToFile(List<String> stringList, String filePath) {
//        try (FileWriter fileWriter = new FileWriter(filePath);
//             BufferedWriter writer = new BufferedWriter(fileWriter)) {
//
//            // Add a new line before writing the list
//            writer.newLine();
//
//            for (String line : stringList) {
//                writer.write(line);
//                writer.newLine(); // Add a newline character after each line
//            }
//
//            // Add a new line after writing the list
//            writer.newLine();
//
//            System.out.println("Successfully wrote the list to the file: " + filePath);
//        } catch (IOException e) {
//            System.err.println("Error writing the list to the file: " + e.getMessage());
//        }
//    }
    public static String getTitleFromUrl(String url) {
        try {
            Document document = Jsoup.connect(url).get();
            return document.title().toLowerCase();
        } catch (IOException e) {
            e.printStackTrace();
            return null; // or handle the error in a way that makes sense for your application
        }
    }
    public static String getBodyTextFromUrl(String url) {
        try {
            Document document = Jsoup.connect(url).get();
            return document.body().text().toLowerCase();
        } catch (IOException e) {
            e.printStackTrace();
            return null; // or handle the error in a way that makes sense for your application
        }
    }
//    public static String getBodyTextFromUrl(String url) {
//    try {
//        Connection.Response response = Jsoup.connect(url).execute();
//
//        // Check HTTP status code
//        int statusCode = response.statusCode();
//        if (statusCode == 403) {
//            System.err.println("HTTP error fetching URL. Status=403, URL=" + url);
//            return null; // Skip processing for URLs with 403 error
//        }
//
//        Document document = response.parse();
//        return document.body().text().toLowerCase();
//    } catch (HttpStatusException e) {
//        System.err.println("HTTP error fetching URL. Status=" + e.getStatusCode() + ", URL=" + url);
//    } catch (IOException e) {
//        e.printStackTrace();
//    }
//    return null;
//}
    private static float calculateProbability(int numerator, int denominator) {
        return denominator > 0 ? (float) numerator / (float) denominator : 0.0f;
    }
//    public static boolean isTopicTerm(List<String> webSites, String subjectLabel, Word potentialTopicTerm) {
//        int numberOfSearchResults = webSites.size();
//        int numberOfSearchResultsWithTopicTerm = 0;
//        int numberOfSearchResultsWithQueryTermsInTitle = 0;
//        int numberOfSearchResultsWithQueryTermsInTitleAndTopicTermInBody = 0;
//
//        for (String webSite : webSites) {
//            boolean topicTermFoundInBody = getBodyTextFromUrl(webSite).contains(potentialTopicTerm.getWord().toLowerCase());
//
//            if (topicTermFoundInBody) {
//                numberOfSearchResultsWithTopicTerm++;
//            }
//
//            if (getTitleFromUrl(webSite).contains(subjectLabel.toLowerCase())) {
//                numberOfSearchResultsWithQueryTermsInTitle++;
//
//                if (topicTermFoundInBody) {
//                    numberOfSearchResultsWithQueryTermsInTitleAndTopicTermInBody++;
//                }
//            }
//        }
//
//        float numberOfSearchResultsWithTopicTermProbability = calculateProbability(numberOfSearchResultsWithTopicTerm, numberOfSearchResults);
//        float numberOfSearchResultsWithQueryTermsInTitleAndTopicTermInBodyProbability = calculateProbability(numberOfSearchResultsWithQueryTermsInTitleAndTopicTermInBody, numberOfSearchResultsWithQueryTermsInTitle);
//
//        return numberOfSearchResultsWithQueryTermsInTitleAndTopicTermInBodyProbability >= numberOfSearchResultsWithTopicTermProbability;
//    }
public static boolean isTopicTerm(List<String> webSites, String subjectLabel, Word potentialTopicTerm) {
    int numberOfSearchResults = webSites.size();
    int numberOfSearchResultsWithTopicTerm = 0;
    int numberOfSearchResultsWithQueryTermsInTitle = 0;
    int numberOfSearchResultsWithQueryTermsInTitleAndTopicTermInBody = 0;

    for (String webSite : webSites) {
        try {
            String bodyText = getBodyTextFromUrl(webSite);
            String title = getTitleFromUrl(webSite);

            // Check if body text contains the potential topic term
            boolean topicTermFoundInBody = bodyText != null && bodyText.contains(potentialTopicTerm.getWord().toLowerCase());

            if (topicTermFoundInBody) {
                numberOfSearchResultsWithTopicTerm++;
            }

            // Check if title contains the subject label
            if (title != null && title.contains(subjectLabel.toLowerCase())) {
                numberOfSearchResultsWithQueryTermsInTitle++;

                // Check if body text also contains the potential topic term
                if (topicTermFoundInBody) {
                    numberOfSearchResultsWithQueryTermsInTitleAndTopicTermInBody++;
                }
            }
        } catch (Exception e) {
            // Handle exceptions (e.g., log or ignore)
            e.printStackTrace();
        }
    }

    float numberOfSearchResultsWithTopicTermProbability = calculateProbability(numberOfSearchResultsWithTopicTerm, numberOfSearchResults);
    float numberOfSearchResultsWithQueryTermsInTitleAndTopicTermInBodyProbability = calculateProbability(numberOfSearchResultsWithQueryTermsInTitleAndTopicTermInBody, numberOfSearchResultsWithQueryTermsInTitle);

    return numberOfSearchResultsWithQueryTermsInTitleAndTopicTermInBodyProbability >= numberOfSearchResultsWithTopicTermProbability;
}
    public static void main(String[] args) throws IOException {

        JsoupCrawlUtil crawlUtil = new JsoupCrawlUtil();
        String wikipediaUrl = "https://en.wikipedia.org/wiki/";
        String path = "/home/user/Downloads/output.txt";
        String entitysurface = "/home/user/Downloads/surface_forms/entities_surfcae.json";
//        String quantitysurface = "/home/user/Downloads/surface_forms/quantities_surfcae.json";
        JsonFileReader entysurface = new JsonFileReader(entitysurface);
//        JsonFileReader qtysurface = new JsonFileReader(quantitysurface);
//        String pageContent = crawlUtil.readPage(url, timeout);

        FileWriter writer = new FileWriter(path);
        int timeout = 2000; // You can adjust the timeout as needed
        try {
            String jsonFilePath = "/home/user/Downloads/22feb_data_294.json";
            FileInputStream inputStream = new FileInputStream(jsonFilePath);
            String everything = IOUtils.toString(inputStream);
            JSONArray jsonarray = new JSONArray(everything);
            inputStream.close();
//jsonarray.length()
//            System.out.println(jsonarray.length());
            googlesearchapi customSearchApi = new googlesearchapi();
            List<String> proof = new ArrayList<>();
            stops stop_word = new stops();
            for (int k = 0; k < 50; k++) {
                try {
                    proof.clear();
                    JSONObject hobbies = jsonarray.getJSONObject(k);
                    ArrayList<String> links = new ArrayList<>();
                    JSONArray s = hobbies.getJSONArray("links");
                    for (int i = 0; i < s.length(); i++) {
//                    System.out.println(s.getString(i));
                        links.add(s.getString(i));
                    }
                    JSONArray pst = hobbies.getJSONArray("predicate");
                    ArrayList<String> pstr = new ArrayList<>();
                    for (int i = 0; i < pst.length(); i++) {
//                    System.out.println(s.getString(i));
                        pstr.add(pst.getString(i));
                    }
                    String query = hobbies.getString("sentence");
                    System.out.println(query);
                    System.out.println(links);
                    writer.write("++++++++++++query+++++++++++++++");
                    writer.write("\n");
                    writer.write(query);
                    writer.write("\n");
                    writer.write("+++++++++++++++++++++++++++");
                    writer.write("\n");
                    JSONObject address = hobbies.getJSONObject("quantity_1");
                    String qstr = address.getString("quantityStr");
                    String estr = address.getString("entityStr");
                    List<String> ent_surface = (List<String>) entysurface.getValueForKey(estr);
//                    List<String> qnt_surface = (List<String>) qtysurface.getValueForKey(qstr);
                    String topic = wikipediaUrl + ent_surface.get(ent_surface.size() - 1);
                    List<String> results = removePdfLinks(customSearchApi.getSearchResults(query));
                    System.out.println(results);
                    String pageCont = crawlUtil.readPage(topic, timeout);
                    List<Word> out = new ArrayList<>();
//                if (pageCont==null) {
//                    System.out.println("Skipping not supported content");
//                }
//                else {
                    List<Word> words = WikipediaPageCrawler.getKeywordsSortedByFrequency(pageCont);

                    for (Word c : words) {
                        String cop = c.getWord();
                        if (!stop_word.isStopWord(cop)) {
                            out.add(c);
                        }
                    }
//                }
                    List<Word> filtered = out.size() >= 20 ? out.subList(0, 20) : out;
                    List<String> tpc = new ArrayList<>();
                    String subj = ent_surface.get(ent_surface.size() - 1);
                    for (Word w : filtered) {
                        boolean p = isTopicTerm(results, subj, w);
                        System.out.println(p);
                        if (p) {
                            tpc.add(w.getWord());
                        }
                    }
                    writer.write("[");

                    for (int i = 0; i < tpc.size(); i++) {
                        writer.write(tpc.get(i));

                        // Add a comma after each element except the last one
                        if (i < tpc.size() - 1) {
                            writer.write(", ");
                        }
                    }

                    writer.write("]");

//                double tcov = customSearchApi.calculateTermRatio();

//                writer.write("\n");
//                writer.write("+++++++++++ent_quant++++++++++++++++");
//                writeListToFile(ent_surface, path);
//                writeListToFile(qnt_surface, path);
//                writer.write("++++++++++++quant_ent++++++++++");
//                writer.write("\n");
//                System.out.println(query);
//                System.out.println(qstr);
//                System.out.println(estr);
                    System.out.println(ent_surface);
//                    System.out.println(qnt_surface);
//                System.out.println(links);


//                writer.write("$$$ Query --- "+query);
//                writer.write("\n");

                    for (int i = 0; i < links.size(); i++) {

//                System.out.println("Link--- " + (i + 1) + ": " + hobbies.getString(i));
                        String url = links.get(i);
//                    System.out.println(url);
                        String pageContent = crawlUtil.readPage(url, timeout);
//                    if (pageContent == null) {
//                        System.out.println("Skipping not supported content");
//                    } else {
                        double trust = customSearchApi.calculateTermRatio(pageContent, tpc);
                        System.out.println(trust);
                        List<String> sentences = StanfordNLPSentenceBoundaryDisambiguation.getSentences(pageContent);
                        int count = 0;
                        for (int j = 0; j < sentences.size(); j++) {
                            String sentence = sentences.get(j).toLowerCase();
                            if (sentence.length() > 500) {
                                continue;
                            }
                            boolean c1 = false;
                            boolean c2 = false;
//                        matchingTokens.clear();

                            for (String token : ent_surface) {
                                if (sentence.contains(token.toLowerCase())) {
                                    c1 = true;
                                }
                            }
                            for (String token : pstr) {
                                if (sentence.contains(token.toLowerCase()) && c1) {
                                    c2 = true;
//                                System.out.println(sentence);
                                }
                            }

                            if (c1 && c2) {
                                proof.add(sentence);
                                writer.write(url);
                                writer.write("\n");
                                writer.write(sentence);
                                writer.write("\n");
                                writer.write("trustworthiness:" + trust);
                                writer.write("\n");
                                count += 1;
                                if (count > 2) {
                                    break;
                                }
//                            System.out.println("both match happen");
//                            System.out.println(sentence);
                            }
                            //matchingTokens.size() > 1 && && sentence.toLowerCase().contains(qstr)
                            // (sentence.toLowerCase().contains(qstr) || sentence.toLowerCase().contains(estr)) sentence.toLowerCase().contains("purchase")
//                        if (object.length()==1){
//                            if ((sentence.contains(estr) || sentence.contains(estr.toLowerCase()))
//                                    && sentence.length()<1000 && matchingTokens.size() == 1) {
//                                count+=1;
//                                writer.write("&&&");
//                                writer.write(sentence);
////                            writer.write("\n");
//                                System.out.println((j + 1) + "=>" + sentence);
//                                writer.write("@@@");
//                                writer.write(url);
////                            writer.write("\n");
//                                writer.write("&&&");
////                            writer.write("\n");
////                         System.out.println("one");
//                            }
//                        }

//            }
//                writer.write("\n");
//                writer.write("*****************************************************");
//                writer.write("\n");
//                writer.write(query);
//                writer.write("\n");
//                writer.write("\n");
//                writer.write("*****************************************************");
//                writer.write("\n");
                        }
//            writer.close();
//                    }
                    }
                    System.out.println(proof);
                    writer.write("\n");
                    writer.write("\n");
                }
                catch (HttpStatusException e) {
                    // Log or handle HTTP status exceptions
                    System.err.println("HTTP error fetching URL. Status=" + e.getStatusCode() + ", URL=" + e.getUrl());
                    continue; // Skip the current iteration and move on to the next one
                }
            }
//            for (String token : proof) {
//                System.out.println(token);
//            }
        }
            catch(Exception e){
                    e.printStackTrace();
                }
        writer.close();
            }
    public static List<String> removePdfLinks(List<String> stringList) {
        return stringList.stream()
                .filter(link -> !link.toLowerCase().endsWith(".pdf"))
                .collect(Collectors.toList());
    }

    }

