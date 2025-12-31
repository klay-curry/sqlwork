"""
FastAPI主应用程序
网上商城系统后端入口
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from config import settings
import traceback

# 导入路由
from api import auth, merchant, user, common

# 创建FastAPI应用实例
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="基于FastAPI的网上商城系统，支持AI推荐和智能经营建议",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 全局异常处理器
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    捕获所有未处理的异常
    """
    error_detail = f"{type(exc).__name__}: {str(exc)}"
    error_trace = traceback.format_exc()
    
    print("=" * 70)
    print(f"Global Exception Handler Caught:")
    print(f"URL: {request.url}")
    print(f"Method: {request.method}")
    print(f"Error: {error_detail}")
    print(f"Traceback:\n{error_trace}")
    print("=" * 70)
    
    return JSONResponse(
        status_code=500,
        content={
            "detail": error_detail,
            "type": type(exc).__name__,
            "traceback": error_trace if settings.DEBUG else None
        }
    )

# 配置CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router)
app.include_router(merchant.router)
app.include_router(user.router)
app.include_router(common.router)


@app.get("/", tags=["根路径"])
def read_root():
    """
    API根路径
    """
    return {
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs_url": "/docs"
    }


@app.get("/health", tags=["健康检查"])
def health_check():
    """
    健康检查接口
    """
    return {
        "status": "healthy",
        "database": "connected"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,  # 禁用reload以避免Python 3.12 Windows Store版本的bug
        log_level="info"
    )
