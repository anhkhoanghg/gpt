#1. Daily task:
#"input_text" :  Remind me to working out everyday at 8 pm.
#"target_text" : <sot><sum>Working out daily<totd>5<spec_time>20:00:00<prio>5<status>0<cate>daily<diff>4<imp>3<exp_min>90<dow>null<day>null<month>null<no_date>null<no_week>null<no_month>null<eot>

#2.Intra day task
#2.1 No specific time
#"input_text" :  Remind me to remember reading email tonight.
#"target_text" : <sot><sum>Checking email<totd>5<spec_time>null<prio>1<status>0<cate>work<diff>5<imp>1<exp_min>60<dow>null<day>null<month>null<no_date>0<no_week>null<no_month>null<eot>
#2.2 Time specified
#"input_text" :  Remind me to remember reading email at 10pm.
#"target_text" : <sot><sum>Checking email<totd>5<spec_time>22:00:00<prio>1<status>0<cate>work<diff>5<imp>1<exp_min>60<dow>null<day>null<month>null<no_date>null<no_week>null<no_month>null<eot>

#3. Within number of week task
#"input_text" :  Assistant note it down for me to prepare my cv next 2 week.
#"target_text" : <sot><sum>Prepare cv<totd>2<spec_time>null<prio>2<status>0<cate>work<diff>3<imp>2<exp_min>120<dow>null<day>null<month>null<no_date>null<no_week>2<no_month>null<eot>

#4. Task within a month task:
#"input_text" :  Finish coding my NLP model before this month.
#"target_text" : <sot><sum>Coding NLP model<totd>4<spec_time>null<prio>2<status>0<cate>work<diff>1<imp>2<exp_min>120<dow>null<day>null<month>null<no_date>null<no_week>null<no_month>0<eot>

#5. Specified day ( day with this month or next n month)
#5.1
#"input_text" :  Remind me to submit my scholarship documents 17 this month .
#"target_text" : <sot><sum>Submit scholarship document<totd>2<spec_time>null<prio>1<status>0<cate>work<diff>2<imp>1<exp_min>60<dow>null<day>17<month>null<no_date>null<no_week>2null<no_month>0<eot>
#5.2
#"input_text" :  Remind me to submit my scholarship documents 17 next month .
#"target_text" : <sot><sum>Submit scholarship document<totd>2<spec_time>null<prio>1<status>0<cate>work<diff>2<imp>1<exp_min>60<dow>null<day>17<month>null<no_date>null<no_week>null<no_month>1<eot>

#Note that, the data begin with token <sot> and end with <eot>. The attributes <diff> (difficulty), <prior>(priority), <imp> (importance) have to value in range 1 - 5 where 1 is the highest value.
#<cate> ( category) is the type of task,
#<exp_min> is the expected amount of time the tasks should be done in minute
#<day>, <month> is specified if the user specifies the day and month the tasks should be done,
#where <no_date>, <no_week> and <no_month> is the number of next date, next week, next month the tasks should be done. Example:
#"I need to done this in the next 2 weeks", then <no_week> is 2, however "I need to done that this week", then <no_week> is 0
#<dow> (day of week) in range 1 - 7, which 1 is sunday,2 is monday (and so on), 7 is saturday. <totd> (time of the day) just follow:
#Midnight: 12:00:00 am - 04:59:59 am (value MidNight)
#Morning: 05:00:00 am - 11:59:59 am (value Morning)
#Noon: 12:00:00 pm - 03:59:59 pm (value Noon)
#Evening: 04:00:00 pm - 07:59:59 pm (value Evening)
#Night: 08:00:00 pm - 11:59:59 pm (value Night)

#If any attributes are not determined, then just give it null value.
