-- CreateEnum
CREATE TYPE "UserRole" AS ENUM ('ADMIN', 'DOCTOR', 'PATIENT_PARENT', 'GUEST');

-- CreateEnum
CREATE TYPE "UserStatus" AS ENUM ('PENDING', 'ACTIVE', 'REJECTED');

-- CreateTable
CREATE TABLE "User" (
    "id" SERIAL NOT NULL,
    "role" "UserRole" NOT NULL,
    "status" "UserStatus" NOT NULL DEFAULT 'PENDING',
    "email" TEXT,
    "fullName" TEXT,
    "passwordHash" TEXT,
    "medicalCouncilId" TEXT,
    "parentId" TEXT,
    "googleSub" TEXT,
    "phoneNumber" TEXT,
    "specialization" TEXT,
    "hospital" TEXT,
    "notes" TEXT,
    "pictureUrl" TEXT,
    "doctorId" INTEGER,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "User_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "User_email_key" ON "User"("email");

-- CreateIndex
CREATE UNIQUE INDEX "User_medicalCouncilId_key" ON "User"("medicalCouncilId");

-- CreateIndex
CREATE UNIQUE INDEX "User_parentId_key" ON "User"("parentId");

-- CreateIndex
CREATE UNIQUE INDEX "User_googleSub_key" ON "User"("googleSub");

-- CreateIndex
CREATE INDEX "User_role_idx" ON "User"("role");

-- CreateIndex
CREATE INDEX "User_status_idx" ON "User"("status");

-- CreateIndex
CREATE INDEX "User_doctorId_idx" ON "User"("doctorId");

-- AddForeignKey
ALTER TABLE "User" ADD CONSTRAINT "User_doctorId_fkey" FOREIGN KEY ("doctorId") REFERENCES "User"("id") ON DELETE SET NULL ON UPDATE CASCADE;
