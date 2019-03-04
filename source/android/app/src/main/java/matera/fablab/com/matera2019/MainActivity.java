package matera.fablab.com.matera2019;

import android.app.Activity;
import android.content.Context;
import android.graphics.Point;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.SurfaceHolder;
import android.view.View;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.RelativeLayout;

import org.apache.http.NameValuePair;
import org.apache.http.message.BasicNameValuePair;

import java.util.ArrayList;
import java.util.List;

public class MainActivity extends Activity implements SurfaceHolder.Callback{

    MySurfaceView mySurfaceView;
    LinearLayout clearBtn;
    LinearLayout saveBtn;
    LinearLayout undoBtn;
    LinearLayout imagesListBtn;
    Context _context;

    String urlSave = "http://www.appius.it/matera/save.php";
    String lineSeparator = "$$";
    String pointSeparator = "-";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        _context = this;

        mySurfaceView = new MySurfaceView(this);
        RelativeLayout mainLayout = (RelativeLayout) findViewById(R.id.mainLayout);
        mainLayout.addView(mySurfaceView);

        clearBtn = findViewById(R.id.clearBtn);
        saveBtn = findViewById(R.id.saveBtn);
        undoBtn = findViewById(R.id.undoBtn);
        imagesListBtn = findViewById(R.id.imagesListBtn);

        clearBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                mySurfaceView.clearAll();
            }
        });

        saveBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                ArrayList<ArrayList<Point>> lines = mySurfaceView.getPicture();

                int dimensioneX = 100;
                int dimensioneY = 100;

                int maxValueX = 0;
                int maxValueY = 0;
                int minValueX = 999999;
                int minValueY = 999999;

                for (ArrayList<Point> line : lines) {
                    for (Point p : line){
                        if (p.x > maxValueX) maxValueX = p.x;
                        if (p.y > maxValueY) maxValueY = p.y;
                        if (p.x < minValueX) minValueX = p.x;
                        if (p.y < minValueY) minValueY = p.y;
                    }
                }

                ArrayList<ArrayList<FloatPoint>> normalizedLines = new ArrayList<>();
                for (ArrayList<Point> line : lines) {
                    ArrayList<FloatPoint> normalizedLine = new ArrayList<>();
                    for (Point p : line){
                        FloatPoint normalizedPoint = new FloatPoint();
                        normalizedPoint.x = ((float)(p.x - minValueX) / (maxValueX - minValueX)) * dimensioneX;
                        normalizedPoint.y = ((float)(p.y - minValueY) / (maxValueY - minValueY)) * dimensioneY;
                        normalizedLine.add(normalizedPoint);
                    }
                    normalizedLines.add(normalizedLine);
                }


                String strPoint = "";

                for (ArrayList<FloatPoint> l : normalizedLines){
                    if (strPoint.length() > 0)
                        strPoint += lineSeparator;
                    String line = "";
                    for (FloatPoint p : l){
                        if (line.length() > 0)
                            line += pointSeparator;
                        line += Float.toString(p.x) + pointSeparator + Float.toString(p.y);
                    }
                    strPoint += line;
                }

                final List<NameValuePair> nameValuePairs = new ArrayList<>();
                nameValuePairs.add(new BasicNameValuePair("points", strPoint));

                Thread networkThread = new Thread(){

                    @Override
                    public void run() {
                        super.run();
                        HttpCall.loadUrl(_context, urlSave, nameValuePairs);
                    }
                };

                networkThread.start();
            }
        });

        undoBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                mySurfaceView.undo();

            }
        });

        imagesListBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {


            }
        });
    }

    @Override
    public void surfaceCreated(SurfaceHolder surfaceHolder) {

    }

    @Override
    public void surfaceDestroyed(SurfaceHolder surfaceHolder) {

    }

    @Override
    public void surfaceChanged(SurfaceHolder surfaceHolder, int i, int i1, int i2) {

    }
}
