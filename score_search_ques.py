
import pandas as pd
import time
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def set_driver(hidden_chrome: bool=False):
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
    options = ChromeOptions()
    options.add_argument('--headless')
    options.add_argument(f'--user-agent={USER_AGENT}') # ブラウザの種類を特定するための文字列
    options.add_argument('log-level=3') # 不要なログを非表示にする
    options.add_argument('--ignore-certificate-errors') # 不要なログを非表示にする
    options.add_argument('--ignore-ssl-errors') # 不要なログを非表示にする
    options.add_experimental_option('excludeSwitches', ['enable-logging']) # 不要なログを非表示にする
    options.add_argument('--incognito') # シークレットモードの設定を付与
    
    service=Service(ChromeDriverManager().install())
    return Chrome(service=service, options=options)

teams_num_list={
    "1":'brooklyn-nets/bsAMUpDO',
    "2":"boston-celtics/KYD9hVEm",
    "3":"new-york-knicks/WCNO4nbt"
}

team_name_list={
    "1":'ネッツ',
    "2":'セルティックス',
    "3":'ニックス',
}

def main():
        team_num=input("表示したいチームの数字を入力してください(半角英数)。終了する場合は×をクリック。\n1 ネッツ,2 セルティックス,3 ニックス...\n>>>")
        selected_team_num=teams_num_list[team_num]
        selected_team_name=team_name_list[team_num]
        driver = set_driver()
        url=f"https://www.flashscore.co.jp/team/{selected_team_num}/results/"
        driver.get(url)
        time.sleep(3)
        name_elems=driver.find_elements(by=By.CSS_SELECTOR,value=".event__participant")
        score_elems=driver.find_elements(by=By.CSS_SELECTOR,value=".event__score")
       
        team_infos=[]
        for name_elem,score_elem in zip(name_elems,score_elems):
            team_infos.append({
                "チーム名":name_elem.text,
                "スコア":score_elem.text
            })
        
        df=pd.DataFrame.from_dict(team_infos)
        df=df[df['チーム名']==str(selected_team_name)]
        max_score=df['スコア'].max()
        min_score=df['スコア'].min()
        
        df=df.sort_values('スコア',ascending=True)
        print(f"{selected_team_name}の直近10試合スコアは、\n最大得点数{max_score}点\n最小得点数{min_score}点\nでした。\n\n\n")
        df.to_csv("試合結果.csv",encoding="utf-8-sig",index=False)

main()
