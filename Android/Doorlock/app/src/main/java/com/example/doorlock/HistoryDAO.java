package com.example.doorlock;

public class HistoryDAO {
    private String historyDate;
    private String user;

    public HistoryDAO(String datetime, String user) {
        this.historyDate = datetime;
        this.user = user;
    }

    public HistoryDAO() {
    }

    public String getUser() {
        return user;
    }

    public void setUser(String user) {
        this.user = user;
    }

    public String getHistoryDate() {
        return historyDate;
    }

    public void setHistoryDate(String historyDate) {
        this.historyDate = historyDate;
    }
}
