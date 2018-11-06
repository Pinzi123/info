
from flask import Flask, render_template, jsonify, Response

import seiya.analysis.job as job
import seiya.analysis.food as food
import seiya.analysis.house as house

app = Flask(__name__)


@app.errorhandler(404)
def not_found(error):
    """404 页面

    """
    return render_template('404.html'), 404


@app.route('/')
def index():
    """首页

    """
    return render_template('index.html')


@app.route('/g2')
def g2():
    """G2 图表示例页

    """
    return render_template('g2.html')


@app.route('/job')
def job_index():
    """拉勾网职位数据分析首页

    """
    return render_template('job/index.html')


@app.route('/job/count-top10')
def job_count_top10():
    """职位数排名前十的城市页面

    """
    return render_template('job/count-top10.html', rows=job.count_top10())


@app.route('/job/count-top10.json')
def job_count_top10_json():
    """职位数排名前十的城市数据

    """
    return jsonify(job.count_top10())


@app.route('/job/salary-top10')
def job_salary_top10():
    """薪资排名前十的城市页面

    """
    return render_template('job/salary-top10.html', rows=job.salary_top10())


@app.route('/job/salary-top10.json')
def job_salary_top10_json():
    """薪资排名前十的城市数据

    """
    return jsonify(job.salary_top10())


@app.route('/job/hot-tags')
def job_hot_tags():
    """热门职位标签页面

    """
    return render_template('job/hot-tags.html', rows=job.hot_tags())


@app.route('/job/hot-tags.json')
def job_hot_tags_json():
    """热门职位标签数据

    """
    return jsonify(job.hot_tags())


@app.route('/job/hot-tags.png')
def job_hot_tags_plot():
    """热门职位标签图片

    """
    return Response(job.hot_tags_plot(format='png'), content_type='image/png')


@app.route('/job/experience-stat')
def job_experience_stat():
    """工作经验统计页面

    """
    return render_template('job/experience-stat.html', rows=job.experience_stat())


@app.route('/job/experience-stat.json')
def job_experience_stat_json():
    """工作经验统计数据

    """
    return jsonify(job.experience_stat())


@app.route('/job/education-stat')
def job_education_stat():
    """学历要求统计页面

    """
    return render_template('job/education-stat.html', rows=job.education_stat())


@app.route('/job/education-stat.json')
def job_education_stat_json():
    """学历要求统计数据

    """
    return jsonify(job.education_stat())


@app.route('/job/salary-by-city-and-education')
def job_salary_by_city_and_education():
    """同等学历不同城市薪资对比页面

    """
    return render_template('job/salary-by-city-and-education.html',
                           rows=job.salary_by_city_and_education())


@app.route('/job/salary-by-city-and-education.json')
def job_salary_by_city_and_education_json():
    """同等学历不同城市薪资对比数据

    """
    return jsonify(job.salary_by_city_and_education())


# 大众点评
@app.route('/restaurant')
def food_index():
    return render_template('food/index.html')


@app.route('/food/hot_res')
def food_hot_res():
    return render_template('food/hot_res.html', rows=food.hot_res())


@app.route('/food/hot_res.json')
def food_hot_res_json():
    return jsonify(food.hot_res())


@app.route('/food/count_top10_lei')
def count_top10_lei():
    return render_template('food/count_top10_lei.html', rows=food.count_top10_lei())


@app.route('/food/count_top10_lei.json')
def count_top10_lei_json():
    return jsonify(food.count_top10_lei())


@app.route('/food/count_top10_quan')
def count_top10_quan():
    return render_template('food/count_top10_quan.html', rows=food.count_top10_quan())


@app.route('/food/count_top10_quan.json')
def count_top10_quan_json():
    return jsonify(food.count_top10_quan())


@app.route('/food/exp_top10_quan')
def exp_top10_quan():
    return render_template('food/exp_top10_quan.html', rows=food.exp_top10_quan())


@app.route('/food/exp_top10_quan.json')
def exp_top10_quan_json():
    return jsonify(food.exp_top10_quan())


@app.route('/food/exp_top10_lei')
def exp_top10_lei():
    return render_template('food/exp_top10_lei.html', rows=food.exp_top10_lei())


@app.route('/food/exp_top10_lei.json')
def exp_top10_lei_json():
    return jsonify(food.exp_top10_lei())


@app.route('/food/fenlei_and_quan')
def fenlei_and_quan():
    return render_template('food/fenlei_and_quan.html', rows=food.fenlei_and_quan())


@app.route('/food/fenlei_and_quan.json')
def fenlei_and_quan_json():
    return jsonify(food.fenlei_and_quan())


# 链家
@app.route('/house')
def house_index():
    return render_template('house/index.html')


@app.route('/house/hot_xiaoqu')
def house_hot_xiaoqu():
    return render_template('house/hot_xiaoqu.html', rows=(house.count_top10()))


@app.route('/house/hot_xiaoqu.json')
def house_hot_xiaoqu_json():
    return jsonify(house.count_top10())


@app.route('/house/hot_huxing')
def house_hot_huxing():
    return render_template('house/hot_huxing.html', rows=(house.all_huxing()))


@app.route('/house/hot_huxing.json')
def house_hot_huxing_json():
    return jsonify(house.all_huxing())


@app.route('/house/area')
def house_area():
    return render_template('house/area.html', rows=(house.all_area()))


@app.route('/house/area.json')
def house_area_json():
    return jsonify(house.all_area())


@app.route('/house/years')
def house_years():
    return render_template('house/years.html', rows=(house.count_years2()))


@app.route('/house/years.json')
def house_years_json():
    return jsonify(house.count_years())


@app.route('/house/most_exp')
def house_most_exp():
    return render_template('house/most_exp.html', rows=(house.price_by_xiaoqu_and_huxing()))


@app.route('/house/most_exp.json')
def house_most_exp_json():
    return jsonify(house.price_by_xiaoqu_and_huxing())


if __name__ == '__main__':
    app.run()
