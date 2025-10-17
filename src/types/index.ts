export interface User {
  id: string;
  username: string;
  email: string;
  fullName: string;
  mobile: string;
  role: UserRole;
  isActive: boolean;
  dateJoined: string;
}

export interface UserRole {
  id: string;
  name: 'admin' | 'employee' | 'customer';
  displayName: string;
  permissions: Permission[];
}

export interface Permission {
  id: string;
  module: string;
  canAdd: boolean;
  canEdit: boolean;
  canDelete: boolean;
  canView: boolean;
}

export interface Employee {
  id: string;
  userId: string;
  fullName: string;
  email: string;
  phone: string;
  roleId: string;
  status: 'active' | 'inactive';
}

export interface Customer {
  id: string;
  userId: string;
  fullName: string;
  mobile: string;
  address: string;
  city: string;
  pincode: string;
  totalOrders: number;
  totalSpent: number;
}

export interface Category {
  id: string;
  name: string;
  createdAt: string;
}

export interface Product {
  id: string;
  name: string;
  categoryId: string;
  category?: Category;
  price: number;
  stock: number;
  description: string;
  image: string;
  nutritionalInfo?: string;
  createdAt: string;
  isActive: boolean;
}

export interface CartItem {
  id: string;
  productId: string;
  product: Product;
  quantity: number;
}

export interface Order {
  id: string;
  customerId: string;
  customer: Customer;
  totalAmount: number;
  paymentMode: 'cod' | 'online';
  paymentStatus: 'pending' | 'paid' | 'failed';
  orderStatus: 'pending' | 'processing' | 'shipped' | 'delivered' | 'cancelled';
  createdAt: string;
  items: OrderItem[];
  shippingAddress: {
    name: string;
    mobile: string;
    email: string;
    address: string;
    city: string;
    pincode: string;
  };
}

export interface OrderItem {
  id: string;
  orderId: string;
  productId: string;
  product: Product;
  quantity: number;
  price: number;
}

export interface ActivityLog {
  id: string;
  userId: string;
  user: User;
  action: string;
  module: string;
  timestamp: string;
}

export interface DashboardStats {
  totalOrders: number;
  totalRevenue: number;
  totalProducts: number;
  totalCustomers: number;
  recentOrders: Order[];
}