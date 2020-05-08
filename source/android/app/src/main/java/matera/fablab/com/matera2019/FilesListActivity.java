package matera.fablab.com.matera2019;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.LinearLayout;
import android.widget.RelativeLayout;
import android.widget.TextView;

import org.apache.http.NameValuePair;

import java.util.List;

public class FilesListActivity extends Activity {

    Context _context;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.files_list);
        _context = this;

        final LinearLayout filesListLayout = findViewById(R.id.filesListLayout);

        Thread networkThread = new Thread(){

            @Override
            public void run() {
                super.run();
                String res = HttpCall.loadUrl(_context, "http://www.appius.it/matera/gcode_files", false);
                String splittedResult[] = res.split("\n");

                for (final String line : splittedResult){

                    Handler mainHandler = new Handler(_context.getMainLooper());

                    Runnable myRunnable = new Runnable() {
                        @Override
                        public void run() {

                            String fileName = line;

                            LayoutInflater inflater = (LayoutInflater)getBaseContext().getSystemService(Context.LAYOUT_INFLATER_SERVICE);
                            RelativeLayout textItemView = (RelativeLayout) inflater.inflate(R.layout.file_item, null);

                            TextView textView = textItemView.findViewById(R.id.textItem);
                            fileName = fileName.replace(".gcode", "");
                            textView.setText(fileName);

                            filesListLayout.addView(textItemView);

                            textView.setOnClickListener(new View.OnClickListener() {
                                @Override
                                public void onClick(View view) {


                                    String fileName = line;
                                    fileName = fileName.replace("gcode", "coord");

                                    Intent i = new Intent(_context, MainActivity.class);
                                    i.putExtra("fileName", fileName);
                                    startActivity(i);

                                }
                            });

                        }
                    };
                    mainHandler.post(myRunnable);



                }

                int asd = 34;
            }
        };

        networkThread.start();

    }

}
