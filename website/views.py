from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Mapping_code, Invest_plan, Users
from . import db
import json

views = Blueprint('views',__name__)

@views.route('/index')
@login_required
def Index():
    print(current_user.id)
    return render_template("index.html", user = current_user)


# 投資取向 (介面)
# ---------------------
# options = 對應 選項文字
# user_plans = 對應 投資計畫 欄位文字
@views.route('/target', methods=['GET','POST'])
@login_required
def Target():
    opCode = Mapping_code.query.filter(Mapping_code.category.in_(['op1','op2','op3'])).all()
    options = list(map(lambda Mapping_code:Mapping_code.serialize(),opCode))
    for i in current_user.investplan:
        i.monInvest_text = mapping_codeValue(i.plan_monthly_invest, options)
        i.planTime_text = mapping_codeValue(i.plan_time, options)
        i.planRisk_text = mapping_codeValue(i.plan_risk, options)
    user_plans = list(map(lambda Invest_plan:Invest_plan.serialize(Invest_plan.id),current_user.investplan))
    return render_template('target.html', user = current_user , options = options, user_plans = user_plans )

# 新增計畫
@views.route('/addnewPlan', methods=['POST'])
@login_required
def Add_newPlan():
    if request.method == 'POST':
        new_planName = request.form.get('new_planName')
        monthlyInvest = request.form.get('monthlyInvest')
        planTime = request.form.get('planTime')
        planRisk = request.form.get('planRisk')
        new_plan = Invest_plan(plan_name=new_planName, plan_monthly_invest=monthlyInvest, plan_time=planTime, plan_risk=planRisk, user_id=current_user.id)
        db.session.add(new_plan)
        db.session.commit()
        return redirect(url_for('views.Target'))
    return jsonify({})

# 刪除計畫
@views.route('/deletePlan', methods=['POST'])
@login_required
def Delete_Plan() -> None:
    plan_id = json.loads(request.data)
    plan = Invest_plan.query.get(plan_id)
    # 確認是否為 計畫主人
    if plan.user_id == current_user.id:
        db.session.delete(plan)
        db.session.commit()
    return jsonify({})

    

@views.route('/portfolio')
@login_required
def Portfolio():
    return render_template('portfolio.html', user = current_user)

@views.route('/picker-oneself')
@login_required
def Picker1():
    return render_template('picker-oneself.html', user = current_user)

@views.route('/picker-cond')
@login_required
def Picker2():
    return render_template('picker-cond.html', user = current_user)

@views.route('/risk-assessment')
@login_required
def Risk_assess():
    return render_template('risk-assessment.html', user = current_user)

@views.route('/account')
@login_required
def Set_account():
    return render_template('account.html', user = current_user)


def mapping_codeValue(id, options):
    for i in options:
        if id == i['id']:
            return i['name']
    return ""
