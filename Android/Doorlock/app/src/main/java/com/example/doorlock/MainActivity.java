package com.example.doorlock;

import android.content.Context;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;

public class MainActivity extends AppCompatActivity {

    private static final String TAG = "DOOR_LOCK_APP";
    ArrayList<HistoryDAO> historyDAOList;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        ListView listView = (ListView)findViewById(R.id.listView);
        Button searchButton = (Button)findViewById(R.id.searchButton);
        Button openButton = (Button)findViewById(R.id.openButton);
        EditText ipEditText = (EditText)findViewById(R.id.ipEditText);


        historyDAOList = new ArrayList<>();
        final MyAdapter myAdapter = new MyAdapter(this, historyDAOList);
        listView.setAdapter(myAdapter);

        listView.setOnItemClickListener((parent, v, position, id) -> Toast.makeText(getApplicationContext(),
                myAdapter.getItem(position).getUser(),
                Toast.LENGTH_LONG).show());

        openButton.setOnClickListener(v -> {
            new Thread(() -> {
                sendPost(ipEditText.getText().toString(), "open", "{\"user\":\"remote\"}");
            }).start();
        });

        searchButton.setOnClickListener(v -> {
            myAdapter.refreshAdapter(historyDAOList);
            new Thread(() -> {
                try {
                    JSONObject jsonObject = sendPost(ipEditText.getText().toString(), "history", "");
                    if(jsonObject != null) {
                        JSONArray historyArray = jsonObject.getJSONArray("history");
                        for (int i = 0; i < historyArray.length(); i++) {
                            JSONObject historyObject = historyArray.getJSONObject(i);

                            HistoryDAO historyDAO = new HistoryDAO();

                            historyDAO.setHistoryDate(historyObject.getString("date"));
                            historyDAO.setUser(historyObject.getString("user"));

                            runOnUiThread(new Runnable() {
                                @Override
                                public void run() {
                                    myAdapter.add(historyDAO);
                                }
                            });
                        }
                    }
                } catch (JSONException e) {
                    e.printStackTrace();
                }
            }).start();

        });

    }

    public JSONObject sendPost(String ip, String path, String params)
    {
        try {
            URL url = new URL("http://" + ip + ":3004/" + path);
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();

            connection.setRequestMethod("POST");
            connection.setRequestProperty("Content-Type", "application/json; charset=utf-8");
            connection.setRequestProperty("Accept", "application/json; charset=utf-8");
            connection.setDoInput(true);
            connection.setDoOutput(true);
            connection.setReadTimeout(1000);
            connection.setConnectTimeout(1500);

            // Send Data
            byte[] outputInBytes = params.getBytes(StandardCharsets.UTF_8);
            OutputStream os = connection.getOutputStream();
            os.write(outputInBytes);
            os.close();

            // Recv Data
            InputStream is = connection.getInputStream();
            BufferedReader br = new BufferedReader(new InputStreamReader(is));
            String line;
            StringBuffer response = new StringBuffer();
            while ((line = br.readLine()) != null) {
                response.append(line);
                response.append('\r');
            }
            br.close();

            String res = response.toString();
            res = res.trim();
            Log.i(TAG, res);


            JSONObject jsonObject = new JSONObject(res);
            return jsonObject;
        }
        catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }

}

class MyAdapter extends BaseAdapter {

    Context mContext;
    LayoutInflater mLayoutInflater;
    ArrayList<HistoryDAO> historyDAOS;

    public MyAdapter(Context context, ArrayList<HistoryDAO> data) {
        mContext = context;
        historyDAOS = data;
        mLayoutInflater = LayoutInflater.from(mContext);
    }

    @Override
    public int getCount() {
        return historyDAOS.size();
    }

    @Override
    public long getItemId(int position) {
        return position;
    }

    @Override
    public HistoryDAO getItem(int position) {
        return historyDAOS.get(position);
    }

    @Override
    public View getView(int position, View converView, ViewGroup parent) {
        View view = mLayoutInflater.inflate(R.layout.history_list_layout, null);

        TextView historyDate = (TextView)view.findViewById(R.id.historyDate);
        TextView user = (TextView)view.findViewById(R.id.user);

        historyDate.setText(historyDAOS.get(position).getHistoryDate());
        user.setText(historyDAOS.get(position).getUser());

        return view;
    }

    public void add(HistoryDAO dao) {
        this.historyDAOS.add(dao);
        notifyDataSetChanged();
    }

    public void refreshAdapter(ArrayList<HistoryDAO> data) {
        this.historyDAOS.clear();
//        this.historyDAOS.addAll(data);
        notifyDataSetChanged();
    }

    public void clearAdapter() {
        this.historyDAOS.clear();
        notifyDataSetChanged();
    }

}
