package matera.fablab.com.matera2019;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.Point;
import android.util.Log;
import android.view.MotionEvent;
import android.view.SurfaceHolder;
import android.view.SurfaceView;

import java.util.ArrayList;

/**
 * Created by Alessandro on 12/06/2018.
 */

public class MySurfaceView extends SurfaceView {

    SurfaceHolder holder;
    Paint paint;
    Context _context;

    public MySurfaceView(Context context) {
        super(context);
        holder = getHolder();
        _context = context;

        setBackgroundColor(Color.WHITE);

        paint = new Paint();

        paint.setARGB(255, 256, 256, 256);
        paint.setStyle(Paint.Style.FILL_AND_STROKE);
        paint.setStrokeWidth(10);
        paint.setAntiAlias(true);
        paint.setDither(false);
        paint.setStrokeJoin(Paint.Join.ROUND);
        paint.setStrokeCap(Paint.Cap.ROUND);
    }

    public void undo() {
        try {
            linesList.remove(linesList.size() - 1);
            invalidate();
        }catch (Exception e){}
    }

    @Override
    protected void onDraw(Canvas canvas) {
        super.onDraw(canvas);

        for (int j = 0; j < linesList.size(); j++){
            ArrayList<Point> l = linesList.get(j);
            for (int i = 0; i < l.size() - 1; i++){
                Point p1 = l.get(i);
                Point p2 = l.get(i + 1);

                canvas.drawLine(p1.x, p1.y, p2.x, p2.y, paint);
            }
        }
    }

    ArrayList<ArrayList<Point> > linesList = new ArrayList<>();
    ArrayList<Point> currentLine;

    boolean isDrawing = false;

    public ArrayList<ArrayList<Point> > getPicture(){
        return linesList;
    }


    public void clearAll(){
        linesList.clear();
        invalidate();
    }

    @Override
    public boolean onTouchEvent(MotionEvent event) {

        float x = event.getX();
        float y = event.getY();

        if (event.getAction() == MotionEvent.ACTION_UP){
            isDrawing = false;
            invalidate();
        }
        else if (event.getAction() == MotionEvent.ACTION_DOWN){
            isDrawing = true;
            currentLine = new ArrayList<>();
            linesList.add(currentLine);
            invalidate();
        }
        else if (event.getAction() == MotionEvent.ACTION_MOVE){

            if (isDrawing == true) {
                Point p = new Point();
                p.set((int) x, (int) y);
                linesList.get(linesList.size() - 1).add(p);
                invalidate();
            }
        }

        return true;
    }
}
