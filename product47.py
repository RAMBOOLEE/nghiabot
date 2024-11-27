import time
from telegram import Update, BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import datetime

# Biến toàn cục lưu thời gian hoạt động và trạng thái của từng người dùng
user_data = {}

# Hàm bắt đầu hoạt động và đếm thời gian
async def start_activity(update: Update, context: ContextTypes.DEFAULT_TYPE, activity: str):
    user_id = update.effective_user.id
    now = time.time()

    # Kiểm tra nếu người dùng đã tham gia hoạt động mà chưa quay lại làm việc
    if user_id in user_data and "current_activity" in user_data[user_id] and user_data[user_id]["current_activity"] != "Work":
        await update.message.reply_text("You have already participated in an activity. Please return to your post before continuing with a new activity..")
        return

    # Nếu người dùng đã có hoạt động trước đó, kết thúc hoạt động cũ
    if user_id in user_data and "current_activity" in user_data[user_id] and user_data[user_id]["current_activity"] != "Work":
        previous_activity = user_data[user_id]["current_activity"]
        start_time = user_data[user_id]["start_time"]
        elapsed_time = now - start_time
        elapsed_minutes = int(elapsed_time // 60)  # Phút
        elapsed_seconds = int(elapsed_time % 60)  # Giây

        await update.message.reply_text(
            f"你已完成活动 {previous_activity}. 总时间: {elapsed_minutes} 分 {elapsed_seconds} 秒."
        )

    # Cập nhật hoạt động mới
    if user_id not in user_data:
        user_data[user_id] = {}
    user_data[user_id]["current_activity"] = activity
    user_data[user_id]["start_time"] = now

    await update.message.reply_text(f"You have started the activity: {activity}.")

# Hàm cài đặt menu lệnh
async def set_commands(application):
    commands = [
        BotCommand("startwork", "Start working"),
        BotCommand("rest", "Take a restTake a rest"),
        BotCommand("eat", "Take a meal break"),
        BotCommand("offwork", "Finish work"),
        BotCommand("back_to_work", "Return to work"),
        BotCommand("total_time", "View total time for activities")  # Lệnh để xem tổng thời gian
    ]
    await application.bot.set_my_commands(commands)

# Hàm cho từng lệnh
async def startwork(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start_activity(update, context, "Startwork")

async def rest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start_activity(update, context, "Rest")

async def eat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start_activity(update, context, "Eat")

async def offwork(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start_activity(update, context, "Offwork")

async def back_to_work(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    now = time.time()

    # Kiểm tra nếu người dùng đang thực hiện hoạt động khác và chưa quay lại làm việc
    if user_id in user_data and "current_activity" in user_data[user_id] and user_data[user_id]["current_activity"] != "工作":
        previous_activity = user_data[user_id]["current_activity"]
        start_time = user_data[user_id]["start_time"]
        elapsed_time = now - start_time
        elapsed_minutes = int(elapsed_time // 60)  # Phút
        elapsed_seconds = int(elapsed_time % 60)  # Giây

        await update.message.reply_text(
            f"You have chosen the activity {previous_activity}.  Total time: : {elapsed_minutes} minutes {elapsed_seconds} seconds."
        )

    # Cập nhật trạng thái làm việc
    user_data[user_id]["current_activity"] = "Work"
    user_data[user_id]["start_time"] = now

    await update.message.reply_text("Return to work.")

# Hàm để xem tổng thời gian hoạt động trong ngày
async def total_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    now = time.time()

    # Kiểm tra nếu người dùng có hoạt động trong ngày
    if user_id not in user_data or "current_activity" not in user_data[user_id]:
        await update.message.reply_text("No activities recorded today.")
        return

    total_time = 0  # Tổng thời gian hoạt động trong ngày
    for activity_data in user_data.values():
        if activity_data.get("start_time"):
            total_time += now - activity_data["start_time"]
    
    # Tính tổng thời gian hoạt động trong ngày
    total_minutes = int(total_time // 60)
    total_seconds = int(total_time % 60)

    await update.message.reply_text(f"Today's total activity time: {total_minutes} minutes {total_seconds} seconds.")

def main():
    # Thay YOUR_TOKEN bằng token bot của bạn
    application = ApplicationBuilder().token("7867490521:AAFprI8-_CQ4jl5tjYo6GVp_m9TycFKFSas").build()

    # Thêm các lệnh xử lý
    application.add_handler(CommandHandler("startwork", startwork))
    application.add_handler(CommandHandler("rest", rest))
    application.add_handler(CommandHandler("eat", eat))
    application.add_handler(CommandHandler("offwork", offwork))
    application.add_handler(CommandHandler("back_to_work", back_to_work))
    application.add_handler(CommandHandler("total_time", total_time))  # Xử lý lệnh xem tổng thời gian

    # Cài đặt menu lệnh
    application.add_handler(CommandHandler("startwork", startwork))  # Đảm bảo thêm handler cho set_commands
    application.add_handler(CommandHandler("rest", rest))  
    application.add_handler(CommandHandler("eat", eat))  
    application.add_handler(CommandHandler("offwork", offwork))  
    application.add_handler(CommandHandler("back_to_work", back_to_work)) 
    application.add_handler(CommandHandler("total_time", total_time))

    # Khởi chạy bot
    application.run_polling()

if __name__ == "__main__":
    main()
