import sys
sys.path.append('/opt/python')          # this needs to be done since LWA loses the path to the layers


def run():
    from osbot_playwright.playwright.fastapi.Fast_API_Playwright import Fast_API_Playwright
    fast_api_playwright = Fast_API_Playwright()
    app = fast_api_playwright.app()

    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

    # from fastapi import FastAPI
    # from pydantic import BaseModel
    #
    # app = FastAPI()
    #
    # class Payload(BaseModel):
    #     method_kwargs:dict
    #     method_name: str
    #     auth_key: str
    #
    #
    # @app.get("/")
    # def root():
    #     return {"message": "Hello from docked_playwright lambda!!!!!"}
    #
    # @app.post("/lambda-shell")
    # def lambda_shell(payload:Payload = None):
    #     try:
    #         if payload:
    #             from osbot_aws.apis.shell.Lambda_Shell import Lambda_Shell
    #             shell_server = Lambda_Shell(dict(payload))
    #
    #             shell_server.valid_shell_request()
    #             if shell_server.valid_shell_request():
    #                 return shell_server.invoke()
    #
    #         return f'lambda shell should be here: {payload}'
    #     except Exception as error:
    #         return str(error)
    #
    # @app.get("/version")
    # def version():
    #     return {"version": "v0.14"}
    #
    # import uvicorn
    # uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == '__main__':
    run()                                  # to be triggered from run.sh