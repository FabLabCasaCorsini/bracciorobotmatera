package matera.fablab.com.matera2019;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.graphics.Point;
import android.os.Bundle;
import android.text.InputType;
import android.view.SurfaceHolder;
import android.view.View;
import android.widget.EditText;
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
    LinearLayout newBtn;
    LinearLayout undoBtn;
    LinearLayout imagesListBtn;
    Context _context;
    String _fileName = "";

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
        newBtn = findViewById(R.id.newBtn);
        undoBtn = findViewById(R.id.undoBtn);
        imagesListBtn = findViewById(R.id.imagesListBtn);

        clearBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {


                new AlertDialog.Builder(_context)
                        .setTitle("Matera 2019")
                        .setMessage("Cancellare il disegno?")
                        .setIcon(android.R.drawable.ic_dialog_alert)
                        .setPositiveButton(android.R.string.yes, new DialogInterface.OnClickListener() {

                            public void onClick(DialogInterface dialog, int whichButton) {
                                mySurfaceView.clearAll();
                            }})
                        .setNegativeButton("No", null).show();

            }
        });


        newBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                new AlertDialog.Builder(_context)
                        .setTitle("Matera 2019")
                        .setMessage("Creare un nuovo disegno?")
                        .setIcon(android.R.drawable.ic_dialog_alert)
                        .setPositiveButton(android.R.string.yes, new DialogInterface.OnClickListener() {

                            public void onClick(DialogInterface dialog, int whichButton) {

                                _fileName = null;

                                Intent i = new Intent(_context, MainActivity.class);
                                startActivity(i);
                                finish();

                            }})
                        .setNegativeButton("No", null).show();

            }
        });


        saveBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {


                new AlertDialog.Builder(_context)
                        .setTitle("Matera 2019")
                        .setMessage("Salvare il disegno?")
                        .setIcon(android.R.drawable.ic_dialog_alert)
                        .setPositiveButton(android.R.string.yes, new DialogInterface.OnClickListener() {

                            public void onClick(DialogInterface dialog, int whichButton) {


                                AlertDialog.Builder builder = new AlertDialog.Builder(_context);
                                builder.setTitle("Inserisci un titolo");

                                final EditText input = new EditText(_context);
                                input.setInputType(InputType.TYPE_CLASS_TEXT);
                                builder.setView(input);

                                if (_fileName != ""){
                                    saveWithName(_fileName);
                                }
                                else {
                                    builder.setPositiveButton("OK", new DialogInterface.OnClickListener() {
                                        @Override
                                        public void onClick(DialogInterface dialog, int which) {
                                            final String title = input.getText().toString();

                                            saveWithName(title);

                                        }
                                    });
                                    builder.setNegativeButton("Cancel", new DialogInterface.OnClickListener() {
                                        @Override
                                        public void onClick(DialogInterface dialog, int which) {
                                            dialog.cancel();
                                        }
                                    });

                                    builder.show();

                                }


                            }})
                        .setNegativeButton("No", null).show();


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

                Intent i = new Intent(_context, FilesListActivity.class);
                startActivity(i);

            }
        });

        Intent intent = getIntent();

        final String fileName = intent.getStringExtra("fileName");
        if (fileName != null){

            Thread networkThread = new Thread() {

                @Override
                public void run() {
                    super.run();
                    String res = HttpCall.loadUrl(_context, "http://www.appius.it/matera/gcodes/" + fileName, false);
                    mySurfaceView.importPictureFile(res);
                    _fileName = fileName;
                }
            };

            networkThread.start();

        }
    }


    public void saveWithName(String title){

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



        // for (ArrayList<Point> l : lines){
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



        String fileToServer = _fileName;
        String splittedName[] = fileToServer.split("[.]");
        fileToServer = splittedName[0];

        final List<NameValuePair> nameValuePairs = new ArrayList<>();
        nameValuePairs.add(new BasicNameValuePair("title", title));
        nameValuePairs.add(new BasicNameValuePair("points", strPoint));
        nameValuePairs.add(new BasicNameValuePair("fileName", fileToServer));

        Thread networkThread = new Thread(){

            @Override
            public void run() {
                super.run();
                HttpCall.loadUrl(_context, urlSave, nameValuePairs);
            }
        };

        networkThread.start();

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
