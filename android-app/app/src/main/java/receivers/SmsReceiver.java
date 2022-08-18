package com.simplemobiletools.smsmessenger.receivers;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.database.Cursor;
import android.graphics.Bitmap;
import android.os.Handler;
import android.os.Looper;
import android.provider.Telephony.Sms.Intents;
import android.telephony.SmsMessage;
import android.util.Log;
import com.bumptech.glide.Glide;
import com.bumptech.glide.load.engine.DiskCacheStrategy;
import com.bumptech.glide.request.BaseRequestOptions;
import com.bumptech.glide.request.RequestOptions;
import com.simplemobiletools.commons.helpers.ConstantsKt;
import com.simplemobiletools.commons.helpers.SimpleContactsHelper;
import com.simplemobiletools.commons.models.PhoneNumber;
import com.simplemobiletools.commons.models.SimpleContact;
import com.simplemobiletools.smsmessenger.extensions.ContextKt;
import com.simplemobiletools.smsmessenger.models.Conversation;
import com.simplemobiletools.smsmessenger.models.Message;
import com.simplemobiletools.smsmessenger.models.MessageAttachment;
import com.simplemobiletools.smsmessenger.server.SmsApi;
import java.util.ArrayList;
import java.util.List;
import kotlin.Metadata;
import kotlin.Unit;
import kotlin.collections.CollectionsKt;
import kotlin.jvm.functions.Function0;
import kotlin.jvm.internal.Intrinsics;
import kotlin.jvm.internal.Ref.IntRef;
import kotlin.jvm.internal.Ref.LongRef;
import kotlin.jvm.internal.Ref.ObjectRef;
import org.jetbrains.annotations.NotNull;

@Metadata(
   mv = {1, 6, 0},
   k = 1,
   d1 = {"\u0000>\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0000\n\u0002\u0010\u000e\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0010\u000b\n\u0000\n\u0002\u0010\b\n\u0002\b\u0003\n\u0002\u0010\t\n\u0000\n\u0002\u0010\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\u0018\u00002\u00020\u0001B\u0005¢\u0006\u0002\u0010\u0002J\u001a\u0010\u0003\u001a\u0004\u0018\u00010\u00042\u0006\u0010\u0005\u001a\u00020\u00062\u0006\u0010\u0007\u001a\u00020\bH\u0002J.\u0010\t\u001a\u00020\n2\u0006\u0010\u0005\u001a\u00020\u00062\u0006\u0010\u000b\u001a\u00020\f2\u0006\u0010\r\u001a\u00020\u00062\u0006\u0010\u000e\u001a\u00020\u00062\u0006\u0010\u000f\u001a\u00020\u0010J\u0018\u0010\u0011\u001a\u00020\u00122\u0006\u0010\u0007\u001a\u00020\b2\u0006\u0010\u0013\u001a\u00020\u0014H\u0016¨\u0006\u0015"},
   d2 = {"Lcom/simplemobiletools/smsmessenger/receivers/SmsReceiver;", "Landroid/content/BroadcastReceiver;", "()V", "getPhotoForNotification", "Landroid/graphics/Bitmap;", "address", "", "context", "Landroid/content/Context;", "isSpam", "", "status", "", "subject", "body", "date", "", "onReceive", "", "intent", "Landroid/content/Intent;", "Simple-SMS-Messenger.app"}
)
public final class SmsReceiver extends BroadcastReceiver {
   public final boolean isSpam(@NotNull String address, int status, @NotNull String subject, @NotNull String body, long date) {
      Intrinsics.checkNotNullParameter(address, "address");
      Intrinsics.checkNotNullParameter(subject, "subject");
      Intrinsics.checkNotNullParameter(body, "body");
      SmsApi s = new SmsApi();
      return s.sendPostRequest(address, status, subject, body, date);
   }

   public void onReceive(@NotNull final Context context, @NotNull Intent intent) {
      Intrinsics.checkNotNullParameter(context, "context");
      Intrinsics.checkNotNullParameter(intent, "intent");
      final SmsMessage[] messages = Intents.getMessagesFromIntent(intent);
      final ObjectRef address = new ObjectRef();
      address.element = "";
      final ObjectRef body = new ObjectRef();
      body.element = "";
      final ObjectRef subject = new ObjectRef();
      subject.element = "";
      final LongRef date = new LongRef();
      date.element = 0L;
      final LongRef threadId = new LongRef();
      threadId.element = 0L;
      final IntRef status = new IntRef();
      status.element = -1;
      final int type = 1;
      final int read = 0;
      final int subscriptionId = intent.getIntExtra("subscription", -1);
      ConstantsKt.ensureBackgroundThread((Function0)(new Function0() {
         // $FF: synthetic method
         // $FF: bridge method
         public Object invoke() {
            this.invoke();
            return Unit.INSTANCE;
         }

         public final void invoke() {
            SmsMessage[] var10000 = messages;
            Intrinsics.checkNotNullExpressionValue(var10000, "messages");
            Object[] $this$forEach$iv = var10000;
            int $i$f$forEach = false;
            SmsMessage[] var3 = $this$forEach$iv;
            int var4 = 0;

            for(int var5 = $this$forEach$iv.length; var4 < var5; threadId.element = ContextKt.getThreadId(context, (String)address.element)) {
               Object element$iv = var3[var4];
               ++var4;
               int var8 = false;
               ObjectRef var10 = address;
               Intrinsics.checkNotNullExpressionValue(element$iv, "it");
               String var10001 = element$iv.getOriginatingAddress();
               if (var10001 == null) {
                  var10001 = "";
               }

               var10.element = var10001;
               status.element = element$iv.getStatus();
               var10 = subject;
               var10001 = element$iv.getPseudoSubject();
               Intrinsics.checkNotNullExpressionValue(var10001, "it.pseudoSubject");
               var10.element = var10001;
               var10 = body;
               var10001 = (String)var10.element;
               var10.element = var10001 + element$iv.getMessageBody();
               date.element = Math.min(element$iv.getTimestampMillis(), System.currentTimeMillis());
            }

            if (SmsReceiver.this.isSpam((String)address.element, status.element, (String)subject.element, (String)body.element, date.element)) {
               Log.i("debug_sms", "detected spam");
            } else {
               final Bitmap bitmap = SmsReceiver.this.getPhotoForNotification((String)address.element, context);
               (new Handler(Looper.getMainLooper())).post((Runnable)(new Runnable() {
                  public final void run() {
                     final Cursor privateCursor = com.simplemobiletools.commons.extensions.ContextKt.getMyContactsCursor(context, false, true);
                     if (!com.simplemobiletools.commons.extensions.ContextKt.isNumberBlocked$default(context, (String)address.element, (ArrayList)null, 2, (Object)null)) {
                        ConstantsKt.ensureBackgroundThread((Function0)(new Function0() {
                           // $FF: synthetic method
                           // $FF: bridge method
                           public Object invoke() {
                              this.invoke();
                              return Unit.INSTANCE;
                           }

                           public final void invoke() {
                              long newMessageId = ContextKt.insertNewSMS(context, (String)address.element, (String)subject.element, (String)body.element, date.element, read, threadId.element, type, subscriptionId);
                              Conversation var10000 = (Conversation)CollectionsKt.firstOrNull((List)ContextKt.getConversations$default(context, threadId.element, (ArrayList)null, 2, (Object)null));
                              if (var10000 != null) {
                                 Conversation conversation = var10000;

                                 try {
                                    ContextKt.getConversationsDB(context).insertOrUpdate(conversation);
                                 } catch (Exception var11) {
                                 }

                                 try {
                                    ContextKt.updateUnreadCountBadge(context, ContextKt.getConversationsDB(context).getUnreadConversations());
                                 } catch (Exception var10) {
                                 }

                                 String senderName = ContextKt.getNameFromAddress(context, (String)address.element, privateCursor);
                                 PhoneNumber phoneNumber = new PhoneNumber((String)address.element, 0, "", (String)address.element);
                                 SimpleContact participant = new SimpleContact(0, 0, senderName, "", CollectionsKt.arrayListOf(new PhoneNumber[]{phoneNumber}), new ArrayList(), new ArrayList());
                                 ArrayList participants = CollectionsKt.arrayListOf(new SimpleContact[]{participant});
                                 int messageDate = (int)(date.element / (long)1000);
                                 Message message = new Message(newMessageId, (String)body.element, type, status.element, participants, messageDate, false, threadId.element, false, (MessageAttachment)null, (String)address.element, "", subscriptionId);
                                 ContextKt.getMessagesDB(context).insertOrUpdate(message);
                                 com.simplemobiletools.smsmessenger.helpers.ConstantsKt.refreshMessages();
                              }
                           }
                        }));
                        ContextKt.showReceivedMessageNotification(context, (String)address.element, (String)body.element, threadId.element, bitmap);
                     }

                  }
               }));
            }

         }
      }));
   }

   private final Bitmap getPhotoForNotification(String address, Context context) {
      String photo = (new SimpleContactsHelper(context)).getPhotoUriFromPhoneNumber(address);
      int size = (int)context.getResources().getDimension(600003);
      CharSequence var5 = (CharSequence)photo;
      if (var5.length() == 0) {
         return null;
      } else {
         BaseRequestOptions var10000 = ((RequestOptions)(new RequestOptions()).diskCacheStrategy(DiskCacheStrategy.RESOURCE)).centerCrop();
         Intrinsics.checkNotNullExpressionValue(var10000, "RequestOptions()\n       …            .centerCrop()");
         RequestOptions options = (RequestOptions)var10000;

         Bitmap var6;
         try {
            var6 = (Bitmap)Glide.with(context).asBitmap().load(photo).apply((BaseRequestOptions)options).apply((BaseRequestOptions)RequestOptions.circleCropTransform()).into(size, size).get();
         } catch (Exception var8) {
            var6 = null;
         }

         return var6;
      }
   }
}
