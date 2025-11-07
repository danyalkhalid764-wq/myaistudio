from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import User, Payment
from schemas import PaymentCreateRequest, PaymentCreateResponse, PaymentCallback
from services.easypaisa_service import EasypaisaService
from routes.auth import get_current_user

router = APIRouter()
easypaisa_service = EasypaisaService()

# Single Paid plan pricing
PLAN_PRICES = {
    "Paid": 2000.0  # PKR
}

@router.post("/create", response_model=PaymentCreateResponse)
async def create_payment(
    request: PaymentCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if plan is valid
    if request.plan not in PLAN_PRICES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid plan selected"
        )
    
    # Check if user is already on a paid plan
    if current_user.plan == "Paid":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already has a paid plan"
        )
    
    amount = PLAN_PRICES[request.plan]
    
    # Create payment with Easypaisa
    payment_result = await easypaisa_service.create_payment(
        amount=amount,
        user_id=current_user.id,
        plan=request.plan
    )
    
    if not payment_result["success"]:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=payment_result["error"]
        )
    
    # Save payment record
    payment = Payment(
        user_id=current_user.id,
        amount=amount,
        status="pending",
        transaction_id=payment_result["transaction_id"]
    )
    db.add(payment)
    db.commit()
    
    return PaymentCreateResponse(
        success=True,
        payment_url=payment_result["payment_url"],
        transaction_id=payment_result["transaction_id"]
    )

@router.post("/callback")
async def payment_callback(
    callback_data: PaymentCallback,
    db: Session = Depends(get_db)
):
    """Handle payment callback from Easypaisa"""
    
    # Find the payment record
    payment = db.query(Payment).filter(
        Payment.transaction_id == callback_data.transaction_id
    ).first()
    
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )
    
    # Update payment status
    payment.status = callback_data.status
    
    if callback_data.status == "completed":
        # Update user plan
        user = db.query(User).filter(User.id == payment.user_id).first()
        if user:
            user.plan = "Paid"
            user.daily_voice_count = 0
            user.daily_video_count = 0
    
    db.commit()
    
    return {"status": "success", "message": "Payment status updated"}

@router.get("/history")
async def get_payment_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's payment history"""
    payments = db.query(Payment).filter(Payment.user_id == current_user.id).all()
    
    return [
        {
            "id": payment.id,
            "amount": payment.amount,
            "status": payment.status,
            "transaction_id": payment.transaction_id,
            "created_at": payment.created_at
        }
        for payment in payments
    ]

@router.post("/upgrade")
async def trigger_upgrade(
    plan: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Trigger payment upgrade process"""
    
    if plan not in PLAN_PRICES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid plan selected"
        )
    
    # Create payment request
    request = PaymentCreateRequest(plan=plan, amount=PLAN_PRICES[plan])
    return await create_payment(request, current_user, db)











