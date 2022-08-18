package com.simplemobiletools.smsmessenger.server;

import android.util.Log
import com.squareup.okhttp.MediaType
import com.squareup.okhttp.OkHttpClient
import com.squareup.okhttp.Request
import com.squareup.okhttp.RequestBody
import org.json.JSONObject
import java.net.URL


public class SmsApi {
    var SERVER_URL: String =  "http://10.0.2.2:8000/";
    var CHECK_SPAM: String = "checkSpam";

    fun sendPostRequest(address:String, status:Int, subject:String, body:String, date:Long): Boolean {
        Log.i("debug_sms", "run smsapi");
        val values = mapOf("address" to address, "subject" to subject, "status" to status, "body" to body, "date" to date)

        val jsonObject = JSONObject()
        jsonObject.put("phone_number_send", address)
        jsonObject.put("phone_number_receive", "0912345679")
        jsonObject.put("message_status", status)
        jsonObject.put("message_subject", subject)
        jsonObject.put("message_content", body)
        jsonObject.put("message_date", date)
        //Log.i("debug_sms", jsonObject.toString());

        val url = URL(SERVER_URL)
        val body: RequestBody = RequestBody.create(
            MediaType.parse("application/json"), jsonObject.toString()
        )

        val client = OkHttpClient()
        val request = Request.Builder()
            .url(SERVER_URL)
            .post(body)
            .addHeader("Accept", "application/json")
            .build()
        val response = client.newCall(request).execute()
        val jData = response.body().string()
        val responeObject = JSONObject(jData)
        Log.i("debug_sms", jData);
        if ( responeObject.get("result") == true ) return true;
        return false;



    }
}
