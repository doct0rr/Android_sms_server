package com.example.kriss.smsserver;

import android.telephony.SmsManager;
import android.util.Log;
import android.widget.Toast;

import java.io.IOException;
import java.util.Map;

import fi.iki.elonen.NanoHTTPD;

/**
 * Created by kriss on 4/7/2017.
 */

public class MyServer extends NanoHTTPD {
    private final static int PORT = 8080;

    public MyServer() throws IOException {
        super(PORT);
        start();
        System.out.println( "\nRunning! Point your browers to http://localhost:8080/ \n" );
    }

    @Override
    public Response serve(IHTTPSession session) {

        String msg = "<html><body><h1>Sms server</h1>\n";
        Map<String, String> parms = session.getParms();
        if (parms.get("number") == null && parms.get("message") == null) {

            msg += "<form action='?' method='get'>\n  " +
                    "<p>Number: <input type='text' name='number'>" +
                    "<input type='text' name='message'></p>\n" +
                    "</form>\n";
        } else {
            String phoneNumber = parms.get("number");
            String message = parms.get("message");
            msg += "<p>To, " + parms.get("number") +"sending:"+ parms.get("message")+"!</p>";
            SmsManager smsManager = SmsManager.getDefault();
            smsManager.sendTextMessage(phoneNumber, null, message, null, null);
        }
        return newFixedLengthResponse(msg + "</body></html>\n");
    }


}
