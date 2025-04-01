package org.example;
import java.util.Arrays;
import java.util.List;

public class stops {
    String[] stringsToAdd = {
            ":", " ", "``", "`", "_NE_", "''", ",", "'", "'s", "-LRB-", "-RRB-", ".", "-", "--", "i", "a", "about", "an", "and",
            "are", "as", "at", "be", "but", "by", "com", "for", "from",
            "how", "in", "is", "it", "of", "on", "or", "that", "the", "The", "was", "were", "a",
            "under", "this", "to", "what", "when", "where", "who", "will", "with", "the", "www", "before", ",", "after", ";", "like", "and",
            "disambiguation", "http", "retrieved", "com", "how", "in", "is", "it", "of", "on", "or", "that", "the", "The", "was", "were", "him", "his", "her", "she", "into", "they",
            "this", "to", "what", "when", "where", "who", "will", "with", "the", "www", "before", ",", "after", ";", "like", "and",
            "xml" , "www", "html", "wikipedia", "link", "links", "isbn", "en", "jp",
            "edit", "article", "world", "articles", "history", "free", "contact", "bearbeiten",
            "changes", "pages", "news", "january", "february", "march", "april", "wurden",
            "may", "june", "july", "august", "september", "october", "november", "original",
            "december", "org", "categories", "sources", "st", "one", "page", "new", "archived","which","had","would","doi","bibcode","he",
            "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
            "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"

};
    List<String> stringsList = Arrays.asList(stringsToAdd);
    public boolean isStopWord(String token) {
        return stringsList.contains(token);
    }
}
