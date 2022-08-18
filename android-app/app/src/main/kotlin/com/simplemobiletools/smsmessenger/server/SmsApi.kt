package com.simplemobiletools.smsmessenger.server;

import android.util.Log
//import com.squareup.okhttp.MediaType
//import com.squareup.okhttp.OkHttpClient
//import com.squareup.okhttp.Request
//import com.squareup.okhttp.RequestBody
import okhttp3.MediaType
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody
import org.json.JSONObject
import java.net.URL

public class SmsApi {
    var SERVER_URL: String =  "http://10.0.2.2:8000/sms/classifier";
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
//        val mediaType = "application/json; charset=utf-8".toMediaType()
        val body: RequestBody = RequestBody.create(
            "application/json".toMediaTypeOrNull(), jsonObject.toString()
        )

        val client = OkHttpClient()
        val request = Request.Builder()
            .url(SERVER_URL)
            .post(body)
            .addHeader("Accept", "application/json")
            .build()
        val response = client.newCall(request).execute()
        val jData = response.body
        if ( jData != null ){
            val v = jData.string();
//            val responeObject = JSONObject(jData)
            Log.i("debug_sms", v);
//            if (responeObject.get("result") == true) return true;
            if ( "spam" in v ) return true;
            return false;
        }
        else{
            return false;
        }
    }
}
